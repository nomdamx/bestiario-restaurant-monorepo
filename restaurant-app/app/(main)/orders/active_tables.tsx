import { View, Text, Pressable, FlatList } from "react-native";
import { useState, useEffect } from "react";
import type { APIResponse, RestaurantTable, Ticket } from "types/api_types";
import Constants from "expo-constants";
import { router } from "expo-router";
import { TableCardActive } from "components/TableCardActive";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";
import { spacing, spacingHelpers } from "styles/tokens";
import { useAuth } from "hooks/AuthContext";

type TableGroup = {
    [table_number: string]: {
        data_table: RestaurantTable;
        grouped_tickets: Ticket[];
    };
};

export default function TablesActive() {
    const [tickets, setTicktets] = useState<Ticket[]>([]);
    const [groupedTables, setGroupedTables] = useState<TableGroup>({});
    const [cargando, setCargando] = useState(true);
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { authFetch } = useAuth();

    async function fetchTickets() {
        try {
            const api_response: APIResponse<Ticket> = await authFetch(
                API_URL +
                    "ticket/?relations=true&is_active=true&filter_field=is_paid&filter_value=false",
                {
                    method: "GET",
                },
            ).then((response) => response.json());

            setTicktets(api_response.response);
        } catch (error) {
            console.log(String(error));
            setTicktets([]);
        } finally {
            setCargando(false);
        }
    }

    useEffect(() => {
        setCargando(true);
        fetchTickets();
    }, []);

    function groupTables() {
        const group: TableGroup = {};

        tickets.forEach((ticket) => {
            const table_number = String(ticket.restaurant_table.number);
            if (!group[table_number]) {
                group[table_number] = {
                    data_table: ticket.restaurant_table,
                    grouped_tickets: [],
                };
            }
            group[table_number].grouped_tickets.push(ticket);
        });
        return group;
    }

    useEffect(() => {
        setGroupedTables(groupTables());
    }, [tickets]);

    if (tickets.length <= 0) {
        return (
            <>
                <Pressable
                    onPress={() => router.replace("/")}
                    style={({ pressed }) => [
                        global_container_style.backButton,
                        pressed && forms_style.pressedEffect,
                    ]}
                >
                    <Text style={global_container_style.backButtonText}>
                        Regresar
                    </Text>
                </Pressable>
                <View
                    style={[
                        global_container_style.main_container,
                        {
                            paddingVertical: spacingHelpers.section,
                            gap: spacingHelpers.section,
                            paddingHorizontal: spacing.md,
                        },
                    ]}
                >
                    <Text>
                        {cargando ? "Cargando..." : "No hay Pedidos Abiertos"}
                    </Text>
                </View>
            </>
        );
    }

    return (
        <View style={{ flex: 1 }}>
            <Pressable
                onPress={() => router.push("/orders/")}
                style={({ pressed }) => [
                    global_container_style.backButton,
                    pressed && forms_style.pressedEffect,
                ]}
            >
                <Text style={global_container_style.backButtonText}>
                    Regresar
                </Text>
            </Pressable>
            <FlatList
                data={Object.values(groupedTables)}
                numColumns={2}
                keyExtractor={(item) => `table-${item.data_table.id}`}
                renderItem={({ item }) => (
                    <TableCardActive
                        tickets={item.grouped_tickets}
                        table={item.data_table}
                        isForPrinted={false}
                    />
                )}
                contentContainerStyle={global_container_style.gridContainer}
                columnWrapperStyle={global_container_style.columnWrapper}
                style={{ flex: 1 }}
            />
        </View>
    );
}

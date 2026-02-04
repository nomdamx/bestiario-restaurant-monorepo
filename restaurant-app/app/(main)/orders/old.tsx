import { ScrollView, StyleSheet, View, Text, Pressable } from "react-native";
import { useState, useEffect } from "react";
import type {
    APIResponse,
    PrintTicket,
    RestaurantTable,
    Ticket,
} from "types/api_types";
import { PrintTicketCard } from "components/PrintedTicketCard";
import Constants from "expo-constants";
import { router } from "expo-router";
import { TableCardActive } from "components/TableCardActive";
import { useAuth } from "hooks/AuthContext";

type TableGroup = {
    [table_number: string]: {
        data_table: RestaurantTable;
        grouped_tickets: Ticket[];
    };
};

export default function OrdersOld() {
    const [printTickets, setPrintTickets] = useState<PrintTicket[]>([]);
    const [groupedTables, setGroupedTables] = useState<TableGroup>({});
    const [cargando, setCargando] = useState(true);
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { authFetch } = useAuth();

    async function fetchTickets() {
        try {
            const api_response: APIResponse<PrintTicket> = await authFetch(
                API_URL +
                    "print-ticket/?relations=true&filter_field=printed&filter_value=true",
                {
                    method: "GET",
                },
            ).then((response) => response.json());
            setPrintTickets(api_response.response);
        } catch (error) {
            console.log(String(error));
            setPrintTickets([]);
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

        printTickets.forEach((print_ticket) => {
            const table_number = String(
                print_ticket.ticket.restaurant_table.number,
            );
            if (!group[table_number]) {
                group[table_number] = {
                    data_table: print_ticket.ticket.restaurant_table,
                    grouped_tickets: [],
                };
            }
            group[table_number].grouped_tickets.push(print_ticket.ticket);
        });
        return group;
    }

    useEffect(() => {
        setGroupedTables(groupTables());
    }, [printTickets]);

    if (printTickets.length <= 0) {
        return (
            <>
                <Pressable
                    onPress={() => router.replace("/")}
                    style={({ pressed }) => [
                        headerStyle.backButton,
                        pressed && actionStyle.pressedEffect,
                    ]}
                >
                    <Text style={headerStyle.backButtonText}>Regresar</Text>
                </Pressable>
                <View style={style.container}>
                    <Text>
                        {cargando
                            ? "Cargando..."
                            : "No hay Tickets por Mostrar"}
                    </Text>
                </View>
            </>
        );
    }

    return (
        <>
            <Pressable
                onPress={() => router.push("/orders/")}
                style={({ pressed }) => [
                    headerStyle.backButton,
                    pressed && actionStyle.pressedEffect,
                ]}
            >
                <Text style={headerStyle.backButtonText}>Regresar</Text>
            </Pressable>
            <ScrollView contentContainerStyle={style.container}>
                {printTickets
                    .filter((t) => t.print_for_pay === true)
                    .sort((a, b) => b.id - a.id)
                    .map((t) => (
                        <PrintTicketCard key={t.id} printed_ticket={t} />
                    ))}
            </ScrollView>
            {/* <FlatList
                data={Object.values(groupedTables)}
                numColumns={2}
                keyExtractor={(item) => `table-${item.data_table.id}`}
                renderItem={({ item }) => (
                    <TableCardActive
                        tickets={item.grouped_tickets}
                        table={item.data_table}
                        isForPrinted={true}
                    />
                )}
                contentContainerStyle={style.gridContainer}
                columnWrapperStyle={style.columnWrapper}
            /> */}
        </>
    );
}
const style = StyleSheet.create({
    container: {
        flexGrow: 1,
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        paddingVertical: 20,
        gap: 20,
        paddingHorizontal: 16,
    },
    gridContainer: {
        paddingHorizontal: 16,
        paddingTop: 16,
        paddingBottom: 16,
    },
    columnWrapper: {
        justifyContent: "space-between",
        marginBottom: 16,
    },
});

const headerStyle = StyleSheet.create({
    backButton: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 8,
        paddingHorizontal: 10,
        borderRadius: 8,
        alignSelf: "flex-start",
        marginBottom: 8,
        backgroundColor: "#f0f0f0",
        maxWidth: "70%",
    },

    backButtonText: {
        fontSize: 15,
        fontWeight: "500",
        color: "#555",
        marginLeft: 5,
    },
});

const actionStyle = StyleSheet.create({
    pressedEffect: {
        opacity: 0.85,
        transform: [{ scale: 0.97 }],
    },
});

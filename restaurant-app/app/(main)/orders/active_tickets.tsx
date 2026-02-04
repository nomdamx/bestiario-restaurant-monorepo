import { ScrollView, View, Text, Pressable } from "react-native";
import { useState, useEffect } from "react";
import type { APIResponse, Ticket } from "types/api_types";
import { TicketCard } from "components/TicketCard";
import Constants from "expo-constants";
import { router, useLocalSearchParams } from "expo-router";

import { global_container_style } from "styles/global";
import { spacingHelpers, spacing } from "styles/tokens";
import { forms_style } from "styles/forms";
import { useAuth } from "hooks/AuthContext";

export default function OrdersActive() {
    const [tickets, setTicktets] = useState<Ticket[]>([]);
    const { table_number } = useLocalSearchParams();
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
            const sortedTickets = api_response.response
                .filter(
                    (t) => String(t.restaurant_table.number) === table_number,
                )
                .sort(
                    (a, b) =>
                        new Date(b.created_at).getTime() -
                        new Date(a.created_at).getTime(),
                );
            setTicktets(sortedTickets);
            setCargando(false);
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
    }, [table_number]);

    if (tickets.length <= 0) {
        return (
            <>
                <Pressable
                    onPress={() => router.push("/orders/active_tables")}
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
                        {cargando
                            ? "Cargando..."
                            : "No hay Tickets por Mostrar"}
                    </Text>
                </View>
            </>
        );
    }

    return (
        <View style={{ flex: 1 }}>
            <Pressable
                onPress={() => router.push("/orders/active_tables")}
                style={({ pressed }) => [
                    global_container_style.backButton,
                    pressed && forms_style.pressedEffect,
                ]}
            >
                <Text style={global_container_style.backButtonText}>
                    Regresar
                </Text>
            </Pressable>
            <ScrollView
                contentContainerStyle={[
                    global_container_style.scroll_container,
                    {
                        paddingVertical: spacingHelpers.section,
                        gap: spacingHelpers.section,
                        paddingHorizontal: spacing.md,
                    },
                ]}
            >
                {tickets.map((t, idx) => (
                    <TicketCard key={t.uuid} ticket={t} />
                ))}
            </ScrollView>
        </View>
    );
}

import {
    RestaurantTable,
    newTicket,
    APIResponse,
    Ticket,
} from "types/api_types";
import { Pressable, Text, StyleSheet, Alert } from "react-native";
import { IconTable } from "./icons/IconTable";
import { useTicket } from "hooks/TicketContext";
import { router } from "expo-router";
import Constants from "expo-constants";
import { useAuth } from "hooks/AuthContext";
import { User } from "types/auth";

export interface Props {
    table: RestaurantTable;
    user: User | null;
    loading: boolean;
}

export function TableCard({ table, user, loading }: Props) {
    const { setTicket, refreshFromAPI } = useTicket();
    const { authFetch } = useAuth();
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;

    if (loading || !user) return null;

    async function createNewTicket() {
        if (!user) return;

        const new_ticket: newTicket = {
            id_restaurant_table: table.id,
            comments: "",
            id_user: user.id,
        };
        const response_ticket = await authFetch(API_URL + "ticket/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(new_ticket),
        });

        if (!response_ticket.ok) {
            throw new Error(`Error HTTP: ${response_ticket.status}`);
        }

        const response: APIResponse<Ticket> = await response_ticket.json();
        const res_ticket = response.response[0];
        setTicket(res_ticket);

        refreshFromAPI(res_ticket.uuid).then(() => {
            router.push({
                pathname: "/orders/[uuid]",
                params: { uuid: res_ticket.uuid },
            });
        });
    }

    async function handleNewTicket() {
        if (!user) return;

        const activeTickets = table.tickets?.filter((t) => !t.is_paid) ?? [];

        if (activeTickets.length === 0) {
            await createNewTicket();
            return;
        }

        if (activeTickets.length === 1) {
            const uuid = activeTickets[0].uuid;

            Alert.alert(
                "Pedido activo",
                "Esta mesa ya tiene un pedido activo. ¿Qué deseas hacer?",
                [
                    { text: "Cancelar", style: "cancel" },
                    {
                        text: "Ver pedido",
                        onPress: () =>
                            router.push({
                                pathname: "/orders/[uuid]",
                                params: { uuid },
                            }),
                    },
                    {
                        text: "Crear nuevo",
                        style: "destructive",
                        onPress: () => createNewTicket(),
                    },
                ],
            );

            return;
        }

        Alert.alert(
            "Pedidos activos",
            "Esta mesa tiene varios pedidos activos. ¿Qué deseas hacer?",
            [
                { text: "Cancelar", style: "cancel" },
                {
                    text: "Ver pedidos",
                    onPress: () =>
                        router.push({
                            pathname: "/orders/active_tickets",
                            params: { table_number: table.number },
                        }),
                },
                {
                    text: "Crear nuevo",
                    style: "destructive",
                    onPress: () => createNewTicket(),
                },
            ],
        );
    }

    return (
        <Pressable
            onPress={handleNewTicket}
            style={({ pressed }) => [
                style.card,
                pressed && style.pressed,
                { width: "48%" },
            ]}
        >
            <Text style={style.cardText}>Mesa #{table.number}</Text>
            <IconTable height={90} />
        </Pressable>
    );
}
const style = StyleSheet.create({
    card: {
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: 12,
        backgroundColor: "#ffffff",
        borderRadius: 14,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.12,
        shadowRadius: 18,
        elevation: 6,
    },
    pressed: {
        transform: [{ scale: 0.97 }],
        opacity: 0.85,
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.08,
        shadowRadius: 10,
        elevation: 3,
    },
    cardText: {
        fontSize: 16,
        fontWeight: "600",
        textAlign: "center",
        marginBottom: 10,
        color: "#333",
    },
});

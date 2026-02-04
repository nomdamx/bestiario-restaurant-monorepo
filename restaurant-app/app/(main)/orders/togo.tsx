import { View, Text } from "react-native";
import { router } from "expo-router";
import {
    newTicket,
    APIResponse,
    Ticket,
    RestaurantTable,
} from "types/api_types";
import { useTicket } from "hooks/TicketContext";
import { useEffect } from "react";
import Constants from "expo-constants";
import { useAuth } from "hooks/AuthContext";

import { global_container_style } from "styles/global";

export default function ToGo() {
    const { setTicket, refreshFromAPI } = useTicket();
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { user, loading, authFetch } = useAuth();

    if (loading || !user) return null;

    async function handleNewTicket() {
        if (!user) return;

        const response_togo = await authFetch(
            API_URL + "restaurant-table/?filter_field=number&filter_value=0",
            {
                method: "GET",
            },
        );

        if (!response_togo.ok) {
            throw new Error(`Error HTTP: ${response_togo.status}`);
        }

        const togo_response: APIResponse<RestaurantTable> =
            await response_togo.json();

        const res_togo_table: RestaurantTable = togo_response.response[0];

        const new_ticket: newTicket = {
            id_restaurant_table: res_togo_table.id,
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

    useEffect(() => {
        handleNewTicket();
    }, []);

    return (
        <View style={global_container_style.main_container}>
            <Text>Cargando ...</Text>
        </View>
    );
}

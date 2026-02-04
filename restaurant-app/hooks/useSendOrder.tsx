import { newOrder } from "types/api_types";
import { useState } from "react";
import { useTicket } from "./TicketContext";
import Constants from "expo-constants";
import { useAuth } from "./AuthContext";

export function useSendOrder() {
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { ticket, refreshFromStorage } = useTicket();
    const [response, setResponse] = useState();
    const [error, setError] = useState<string | null>(null);
    const { authFetch } = useAuth();

    async function send(order: newOrder | null) {
        if (!order || order.quantity <= 0 || !ticket) return;

        refreshFromStorage();
        try {
            const path = API_URL + "order/";
            const response = await authFetch(path, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(order),
            });
            const json = await response.json();
            setResponse(json);
            return json;
        } catch (error) {
            setError(String(error));
        }
    }

    return {
        sendOrder: send,
        response,
        error,
    };
}

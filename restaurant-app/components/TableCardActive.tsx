import {
    RestaurantTable,
    newTicket,
    APIResponse,
    Ticket,
} from "types/api_types";
import { Pressable, Text, StyleSheet } from "react-native";
import { IconTable } from "./icons/IconTable";
import { useTicket } from "hooks/TicketContext";
import { router } from "expo-router";
import Constants from "expo-constants";
import { useAuth } from "hooks/AuthContext";
import { useEffect, useState } from "react";

export interface Props {
    tickets: Ticket[];
    table: RestaurantTable;
    isForPrinted: boolean;
}

export function TableCardActive({ tickets, table, isForPrinted }: Props) {
    const { user, loading } = useAuth();
    const [tableName, setTableName] = useState("Mesa #" + table.number);

    function handleViewTicket(uuid: string) {
        router.push({
            pathname: "/orders/[uuid]",
            params: { uuid: uuid, isForPrinted: String(isForPrinted) },
        });
    }
    function handleViewMultiple(table_number: string) {
        router.push({
            pathname: "/orders/active_tickets",
            params: { table_number: table_number },
        });
    }

    useEffect(() => {
        if (table.number === 99) setTableName("Mesa Imperial");
        if (table.number === 0) setTableName("Para Llevar");
        else return;
    }, [table.number]);

    if (loading || !user) return null;

    if (tickets.length === 1) {
        return (
            <Pressable
                onPress={() => handleViewTicket(tickets[0].uuid)}
                style={({ pressed }) => [
                    style.card,
                    pressed && style.pressed,
                    { width: "48%" },
                ]}
            >
                <Text style={style.cardText}>{tableName}</Text>
                <IconTable height={90} />
            </Pressable>
        );
    }

    return (
        <Pressable
            onPress={() => handleViewMultiple(String(table.number))}
            style={({ pressed }) => [
                style.card,
                pressed && style.pressed,
                { width: "48%" },
            ]}
        >
            <Text style={style.cardText}>{tableName}</Text>
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

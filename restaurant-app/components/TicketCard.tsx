import { Text, StyleSheet, Pressable } from "react-native";
import type { Ticket } from "types/api_types";
import { TimerText } from "./TimerText";
import { router } from "expo-router";

export interface Props {
    ticket: Ticket;
}

export function TicketCard({ ticket }: Props) {
    return (
        <Pressable
            style={style.container}
            onPress={() =>
                router.push({
                    pathname: "/orders/[uuid]",
                    params: { uuid: ticket.uuid },
                })
            }
        >
            <Text style={style.text}>
                {ticket.restaurant_table.number === 0
                    ? "Para Llevar"
                    : "Mesa #" + ticket.restaurant_table.number}
            </Text>
            <Text style={style.text}>Ticket: {ticket.ticket_number}</Text>
            <Text style={style.text}>
                Tiempo: <TimerText timestamp={ticket.created_at} />
            </Text>
        </Pressable>
    );
}

const style = StyleSheet.create({
    container: {
        backgroundColor: "#ffffff",
        paddingVertical: 18,
        paddingHorizontal: 16,
        borderRadius: 14,
        width: "90%",
        maxWidth: 400,
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",

        // ios
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.12,
        shadowRadius: 18,

        // android
        elevation: 6,
    },
    text: {
        fontSize: 18,
        fontWeight: "600",
        textAlign: "center",
        marginVertical: 2,
    },
});

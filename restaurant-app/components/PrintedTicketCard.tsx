import { Text, StyleSheet, Pressable } from "react-native";
import type { PrintTicket } from "types/api_types";
import { TimerText } from "./TimerText";
import { router } from "expo-router";

export interface Props {
    printed_ticket: PrintTicket;
}

export function PrintTicketCard({ printed_ticket }: Props) {
    return (
        <Pressable
            style={style.container}
            onPress={() =>
                router.push({
                    pathname: "/orders/printed/[uuid]",
                    params: {
                        uuid: printed_ticket.ticket.uuid,
                    },
                })
            }
        >
            <Text style={style.text}>
                {printed_ticket.ticket.restaurant_table.number === 0
                    ? "Para Llevar"
                    : "Mesa #" + printed_ticket.ticket.restaurant_table.number}
            </Text>
            <Text style={style.text}>
                Ticket: {printed_ticket.ticket.ticket_number}
            </Text>
            <Text style={style.text}>
                Tiempo:
                <TimerText timestamp={printed_ticket.ticket.created_at} />
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

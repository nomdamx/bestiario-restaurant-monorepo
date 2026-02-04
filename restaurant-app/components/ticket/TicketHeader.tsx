import { Text, View } from "react-native";
import { useTicket } from "hooks/TicketContext";

import { ticket_style } from "styles/ticket";

export default function TicketHeader() {
    const { ticket } = useTicket();

    if (ticket === null) {
        return (
            <View style={ticket_style.headerContainer}>
                <Text style={ticket_style.headerText}>Cargando ...</Text>
            </View>
        );
    }
    return (
        <View style={ticket_style.headerContainer}>
            <Text style={ticket_style.headerText}>
                {ticket.restaurant_table.number === 0
                    ? "Para Llevar"
                    : "Mesa: " + ticket.restaurant_table.number}
                {" - "}
                Mesero: {ticket.user.username}
            </Text>

            <Text style={ticket_style.headerText}>UUID: {ticket.uuid}</Text>
        </View>
    );
}

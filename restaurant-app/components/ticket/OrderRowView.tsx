import { Text, View, Pressable, Alert } from "react-native";
import type { Order } from "types/api_types";
import { useTicket } from "hooks/TicketContext";
import { ticket_style, ticket_row_style } from "styles/ticket";

interface RowProps {
    order: Order;
    triggerToSend: number;
}

export default function OrderRowView({ order, triggerToSend }: RowProps) {
    const { removeOrder, syncingTicket } = useTicket();

    function confirmDelete() {
        Alert.alert(
            "Eliminar producto",
            "¿Seguro que deseas eliminar este producto del ticket?",
            [
                { text: "Cancelar", style: "cancel" },
                {
                    text: "Eliminar",
                    style: "destructive",
                    onPress: () => removeOrder(order.id),
                },
            ],
        );
    }

    return (
        <View style={ticket_style.tableRow}>
            <Pressable
                disabled={syncingTicket}
                onPress={confirmDelete}
                style={({ pressed }) => [
                    ticket_row_style.deleteButton,
                    pressed && ticket_row_style.deleteButtonPressed,
                    syncingTicket && ticket_row_style.deleteButtonDisabled,
                ]}
                hitSlop={8}
            >
                <Text style={ticket_row_style.deleteButtonText}>×</Text>
            </Pressable>
            <View style={[ticket_row_style.column, { flex: 2 }]}>
                <Text
                    style={ticket_row_style.textProduct}
                    pointerEvents="none"
                    numberOfLines={2}
                    ellipsizeMode="tail"
                >
                    {order.product.name}
                </Text>
                <View style={ticket_row_style.addonsRow}>
                    {order.order_addons.map((ad, idx) => (
                        <Text
                            key={"order-addon-" + ad.id}
                            style={ticket_row_style.textAddon}
                            pointerEvents="none"
                            numberOfLines={1}
                            ellipsizeMode="tail"
                        >
                            {ad.product_addons.name}
                            {idx < order.order_addons.length - 1 ? ", " : ""}
                        </Text>
                    ))}
                </View>
            </View>

            <View
                style={[
                    ticket_row_style.column,
                    { flex: 1, justifyContent: "center", alignItems: "center" },
                ]}
            >
                <Text
                    style={ticket_row_style.quantityText}
                    pointerEvents="none"
                >
                    {order.quantity}
                </Text>
            </View>

            <View
                style={[
                    ticket_row_style.column,
                    { flex: 1.5, alignItems: "flex-end" },
                ]}
            >
                <Text style={ticket_row_style.totalText} pointerEvents="none">
                    ${order.total}
                </Text>
            </View>
        </View>
    );
}

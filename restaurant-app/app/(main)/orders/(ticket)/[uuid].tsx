import {
    Text,
    View,
    ScrollView,
    Pressable,
    Alert,
    ActivityIndicator,
    TextInput,
} from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import type { APIResponse, Ticket, Order } from "types/api_types";
import { useState, useEffect, useRef } from "react";
import { useTicket } from "hooks/TicketContext";
import { TimerText } from "components/TimerText";
import Constants from "expo-constants";
import { useAuth } from "hooks/AuthContext";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";
import {
    ticket_style,
    ticket_buttons_style,
    ticket_row_style,
} from "styles/ticket";

interface RowProps {
    order: Order;
    triggerToSend: number;
}

function OrderRow({ order, triggerToSend }: RowProps) {
    const { ticket, removeOrder, syncingTicket } = useTicket();

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

export default function TicketView() {
    const { uuid, isForPrinted } = useLocalSearchParams();
    const isForPrintedBool = isForPrinted === "true";
    const {
        ticket,
        payStoredTicket,
        refreshFromAPI,
        syncingTicket,
        setTicket,
        initialized,
        updateClientTicket,
        updateCommentsTicket,
    } = useTicket();

    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const [saveButton, setSaveButton] = useState(0);
    const [ticket_loading, setTicketLoading] = useState(true);
    const [ticketNotFound, setTicketNotFound] = useState(false);
    const [clientName, setClientName] = useState("");
    const [comments, setComments] = useState("");
    const commentsRef = useRef("");
    const { user, authFetch } = useAuth();
    const hasHiddenTopComments =
        comments.trim().length > 0 &&
        (comments.startsWith("\n") || comments.split("\n").length > 3);

    function confirmPay() {
        if (!clientName) {
            Alert.alert(
                "Cobrar",
                "¿Seguro que deseas cobrar este Ticket sin el nombre del cliente?",
                [
                    { text: "Cancelar", style: "cancel" },
                    {
                        text: "Cobrar",
                        style: "destructive",
                        onPress: () => handlePrintForPay(),
                    },
                ],
            );
        } else {
            Alert.alert("Cobrar", "¿Seguro que deseas cobrar este Ticket?", [
                { text: "Cancelar", style: "cancel" },
                {
                    text: "Cobrar",
                    style: "destructive",
                    onPress: () => handlePrintForPay(),
                },
            ]);
        }
    }

    async function fetchTicket() {
        if (!uuid) return;
        setTicketLoading(true);
        setTicketNotFound(false);
        try {
            const api_response: APIResponse<Ticket> = await authFetch(
                API_URL +
                    "ticket/?is_active=true&relations=true&filter_field=uuid&filter_value=" +
                    uuid,
                {
                    method: "GET",
                },
            ).then((response) => response.json());
            const fetched = api_response.response?.[0] ?? null;
            if (!fetched) {
                setTicket(null);
                setTicketNotFound(true);
            } else {
                setTicket(fetched);
            }
        } catch (error) {
            console.log(String(error));
            setTicketNotFound(true);
        } finally {
            setTicketLoading(false);
        }
    }

    async function handleRefresh() {
        if (!ticket) return;
        await refreshFromAPI(ticket?.uuid);
    }

    async function saveClientIfNeeded(force = false) {
        if (!ticket) return;

        if (!force && ticket.client_name === clientName) return;

        await updateClientTicket(clientName);
    }

    async function handleClientChange() {
        if (ticket?.client_name === clientName) return;
        await updateClientTicket(clientName);
    }

    async function saveCommentsIfNeeded(force = false) {
        if (!ticket) return;
        if (ticket?.comments === comments) return;

        const normalized = commentsRef.current
            .replace(/\n{3,}/g, "\n\n")
            .trim();

        if (!force && ticket.comments === normalized) return;

        await updateCommentsTicket(normalized);
    }

    async function handleCommentsChange() {
        await saveCommentsIfNeeded();
    }

    async function flushTicket() {
        await saveClientIfNeeded();
        await saveCommentsIfNeeded();
    }

    async function handlePrintForPay() {
        if (!ticket) return;
        await saveClientIfNeeded(true);
        await saveCommentsIfNeeded(true);

        await new Promise((r) => setTimeout(r, 250));
        const response = await authFetch(
            API_URL + "ticket/" + ticket.uuid + "/print?for_pay=true",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );
        if (!response.ok) {
            alert("No se ha enviado correctamente la peticion de impresion");
        } else {
            payStoredTicket();
            alert("Enviado a imprimir correctamente");
        }
    }

    async function handlePrintTicket() {
        if (!ticket) return;
        await saveCommentsIfNeeded(true);

        await new Promise((r) => setTimeout(r, 250));
        const response = await authFetch(
            API_URL + "ticket/" + ticket.uuid + "/print?for_pay=false",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );
        if (!response.ok) {
            alert("No se ha enviado correctamente la peticion de impresion");
        } else {
            alert("Enviado a imprimir correctamente");
        }
    }

    async function deleteTicket() {
        if (!ticket) return;

        const response = await authFetch(`${API_URL}ticket/${ticket?.id}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            alert(
                "No se ha Borrado correctamnete el Ticket, vuelva a intentarlo",
            );
        } else {
            alert("Borrado Correctamente");
            router.replace("/orders/active_tables");
        }
    }

    async function handleDelete() {
        Alert.alert("Borrar", "¿Seguro que deseas borrar este Ticket?", [
            { text: "Cancelar", style: "cancel" },
            {
                text: "Borrar",
                style: "destructive",
                onPress: () => deleteTicket(),
            },
        ]);
    }

    useEffect(() => {
        if (!initialized) return;
        if (!uuid) return;

        fetchTicket();
    }, [initialized, uuid]);

    useEffect(() => {
        if (ticket?.client_name) {
            setClientName(ticket.client_name);
        }
        if (ticket?.comments) {
            setComments(ticket.comments);
        }
    }, [ticket]);

    if (!initialized || ticket_loading) {
        return (
            <View style={ticket_style.container}>
                <ActivityIndicator />
            </View>
        );
    }

    if (ticketNotFound) {
        return (
            <View style={ticket_style.container}>
                <Text>No se pudo cargar el ticket.</Text>
                <Pressable onPress={fetchTicket}>
                    <Text>Reintentar</Text>
                </Pressable>
            </View>
        );
    }

    if (!ticket) {
        return (
            <View style={ticket_style.container}>
                <ActivityIndicator />
            </View>
        );
    }

    const ticket_total = ticket.total ?? 0;

    return (
        <>
            {syncingTicket && (
                <View style={ticket_style.syncOverlay}>
                    <View style={ticket_style.syncBox}>
                        <ActivityIndicator size="large" />
                        <Text style={ticket_style.syncText}>Cargando...</Text>
                    </View>
                </View>
            )}
            <Pressable
                onPress={() => router.replace("/")}
                style={({ pressed }) => [
                    global_container_style.backButton,
                    pressed && forms_style.pressedEffect,
                ]}
            >
                <Text style={global_container_style.backButtonText}>
                    Regresar
                </Text>
            </Pressable>
            <View style={ticket_style.container}>
                <ScrollView contentContainerStyle={ticket_style.ordersScroll}>
                    <View style={ticket_style.headerContainer}>
                        <Text style={ticket_style.headerText}>
                            {ticket.restaurant_table.number === 0
                                ? "Para Llevar"
                                : "Mesa: " + ticket.restaurant_table.number}
                            {" - "}
                            Mesero: {ticket.user.username}
                            {" - "}
                            Ticket: #{ticket.ticket_number}
                        </Text>

                        <Text style={ticket_style.headerText}>
                            UUID: {ticket.uuid}
                        </Text>

                        <Text style={ticket_style.headerText}>
                            Tiempo: <TimerText timestamp={ticket.created_at} />
                        </Text>
                    </View>
                    <View style={ticket_style.metaSection}>
                        {ticket.restaurant_table.number === 0 && (
                            <View style={ticket_style.clientContainer}>
                                <Text style={ticket_style.clientLabel}>
                                    Cliente
                                </Text>
                                <TextInput
                                    value={clientName}
                                    placeholder="Nombre del cliente"
                                    onChangeText={setClientName}
                                    onBlur={handleClientChange}
                                    style={ticket_style.clientInput}
                                    placeholderTextColor="#999"
                                />
                            </View>
                        )}
                        <View style={[ticket_style.clientContainer]}>
                            <Text style={ticket_style.clientLabel}>
                                Comentarios
                            </Text>

                            {hasHiddenTopComments && (
                                <Text style={ticket_style.moreAboveHint}>
                                    ↑ Hay más comentarios arriba
                                </Text>
                            )}

                            <TextInput
                                value={comments}
                                placeholder="Comentarios del pedido"
                                onChangeText={(text) => {
                                    setComments(text);
                                    commentsRef.current = text;
                                }}
                                onEndEditing={handleCommentsChange}
                                style={ticket_style.commentsInput}
                                placeholderTextColor="#999"
                                multiline
                                numberOfLines={3}
                            />
                        </View>
                    </View>
                    <View style={ticket_style.table}>
                        <View style={ticket_style.tableHeader}>
                            <Text style={[ticket_style.headerCol, { flex: 3 }]}>
                                Producto
                            </Text>
                            <Text style={[ticket_style.headerCol, { flex: 2 }]}>
                                Cantidad
                            </Text>
                            <Text
                                style={[
                                    ticket_style.headerCol,
                                    ticket_style.totalHeader,
                                ]}
                            >
                                Total
                            </Text>
                        </View>
                        <View style={ticket_style.ordersScroll}>
                            {[...ticket.orders]
                                .sort((a, b) => a.id - b.id)
                                .map((or, idx) => (
                                    <OrderRow
                                        key={`order-row-${or.id}`}
                                        order={or}
                                        triggerToSend={saveButton}
                                    />
                                ))}
                        </View>
                        {/* <View
                            style={[
                                ticket_style.tableRow,
                                ticket_style.totalRow,
                            ]}
                        >
                            <Text style={ticket_style.emptyCol}></Text>
                            <Text style={ticket_style.emptyCol}></Text>
                            <Text style={ticket_style.totalAmount}>
                                ${ticket_total}
                            </Text>
                        </View> */}
                    </View>
                </ScrollView>
                <View style={ticket_style.totalBar}>
                    <Text style={ticket_style.totalLabel}>Total</Text>
                    <Text style={ticket_style.totalValue}>${ticket_total}</Text>
                </View>
                <View style={ticket_buttons_style.footer}>
                    <View style={ticket_buttons_style.container}>
                        {(user?.auth_level === "admin" ||
                            user?.auth_level === "manager") && (
                            <Pressable
                                onPress={handleDelete}
                                style={({ pressed }) => [
                                    ticket_buttons_style.baseButton,
                                    pressed &&
                                        ticket_buttons_style.buttonPressed,
                                ]}
                            >
                                <Text
                                    style={[
                                        ticket_buttons_style.text,
                                        forms_style.deleteText,
                                    ]}
                                >
                                    Borrar
                                </Text>
                            </Pressable>
                        )}
                        <Pressable
                            onPress={handleRefresh}
                            style={({ pressed }) => [
                                ticket_buttons_style.baseButton,
                                pressed && ticket_buttons_style.buttonPressed,
                            ]}
                        >
                            <Text style={ticket_buttons_style.text}>
                                Recargar
                            </Text>
                        </Pressable>
                        {!isForPrintedBool && (
                            <Pressable
                                onPress={flushTicket}
                                style={({ pressed }) => [
                                    ticket_buttons_style.baseButton,
                                    pressed &&
                                        ticket_buttons_style.buttonPressed,
                                ]}
                            >
                                <Text style={ticket_buttons_style.text}>
                                    Guardar
                                </Text>
                            </Pressable>
                        )}
                        {!isForPrintedBool && (
                            <Pressable
                                onPress={() => router.push("/orders/menu")}
                                style={({ pressed }) => [
                                    ticket_buttons_style.baseButton,
                                    pressed &&
                                        ticket_buttons_style.buttonPressed,
                                ]}
                            >
                                <Text style={ticket_buttons_style.text}>
                                    Menu
                                </Text>
                            </Pressable>
                        )}

                        {ticket.restaurant_table.number !== 0 &&
                            !isForPrintedBool && (
                                <Pressable
                                    onPress={handlePrintTicket}
                                    style={({ pressed }) => [
                                        ticket_buttons_style.baseButton,
                                        pressed &&
                                            ticket_buttons_style.buttonPressed,
                                    ]}
                                >
                                    <Text style={ticket_buttons_style.text}>
                                        Comandar
                                    </Text>
                                </Pressable>
                            )}
                    </View>
                    <View style={ticket_buttons_style.container}>
                        <Pressable
                            onPress={confirmPay}
                            style={({ pressed }) => [
                                ticket_buttons_style.baseButton,
                                pressed && ticket_buttons_style.buttonPressed,
                            ]}
                        >
                            <Text style={ticket_buttons_style.text}>
                                Cobrar
                            </Text>
                        </Pressable>
                    </View>
                </View>
            </View>
        </>
    );
}

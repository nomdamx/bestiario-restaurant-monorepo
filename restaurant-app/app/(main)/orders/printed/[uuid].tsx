import {
    Text,
    View,
    ScrollView,
    Pressable,
    ActivityIndicator,
} from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import type { APIResponse, Ticket, Order } from "types/api_types";
import { useState, useEffect } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { useTicket } from "hooks/TicketContext";
import { TimerText } from "components/TimerText";
import Constants from "expo-constants";

import { global_container_style } from "styles/global";
import {
    ticket_style,
    ticket_buttons_style,
    ticket_row_style,
} from "styles/ticket";
import { forms_style } from "styles/forms";
import { useAuth } from "hooks/AuthContext";

interface RowProps {
    order: Order;
}

function OrderRow({ order }: RowProps) {
    return (
        <View style={ticket_style.tableRow}>
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

export default function PrintedTicketView() {
    const { uuid } = useLocalSearchParams();
    const { ticket, refreshFromAPI, setTicket, initialized } = useTicket();

    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const [loadingTicket, setLoadingTicket] = useState(true);
    const [ticketNotFound, setTicketNotFound] = useState(false);
    const { authFetch } = useAuth();

    async function fetchTicket() {
        if (!uuid) return;
        setLoadingTicket(true);
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
            setLoadingTicket(false);
        }
    }

    async function handleRefresh() {
        if (!ticket) return;
        await refreshFromAPI(ticket?.uuid);
    }

    async function handlePrintForPay() {
        if (!ticket) return;
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
            alert("Enviado a imprimir correctamente");
        }
    }

    async function handlePrintTicket() {
        if (!ticket) return;
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

    useEffect(() => {
        if (!initialized) return;
        if (!uuid) return;

        fetchTicket();
    }, [initialized, uuid]);

    if (!initialized || loadingTicket) {
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

    if (!ticket || !uuid) {
        return (
            <View style={ticket_style.container}>
                <Text>Cargando...</Text>
            </View>
        );
    }

    const ticket_total = ticket.total ?? 0;

    return (
        <>
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
            <SafeAreaView style={ticket_style.container}>
                <View style={ticket_style.headerContainer}>
                    <Text style={ticket_style.headerText}>
                        {ticket.restaurant_table.number === 0
                            ? "Para Llevar"
                            : " Mesa: " + ticket.restaurant_table.number}
                    </Text>
                    <Text style={ticket_style.headerText}>
                        Mesero: {ticket.user.username}
                    </Text>
                    <Text style={ticket_style.headerText}>
                        Numero de Ticket: {ticket.ticket_number}
                    </Text>
                    <Text style={ticket_style.headerText}>
                        Ticket: {ticket.uuid}
                    </Text>
                    <Text style={ticket_style.headerText}>
                        Tiempo: <TimerText timestamp={ticket.created_at} />
                    </Text>
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
                    <ScrollView
                        contentContainerStyle={ticket_style.ordersScroll}
                    >
                        {[...ticket.orders]
                            .sort((a, b) => a.id - b.id)
                            .map((or, idx) => (
                                <OrderRow
                                    key={`order-row-${or.id}`}
                                    order={or}
                                />
                            ))}
                    </ScrollView>
                    <View
                        style={[ticket_style.tableRow, ticket_style.totalRow]}
                    >
                        <Text style={ticket_style.emptyCol}></Text>
                        <Text style={ticket_style.emptyCol}></Text>
                        <Text style={ticket_style.totalAmount}>
                            ${ticket_total}
                        </Text>
                    </View>
                </View>
                <View style={ticket_buttons_style.container}>
                    <Pressable
                        onPress={handleRefresh}
                        style={({ pressed }) => [
                            ticket_buttons_style.baseButton,
                            pressed && ticket_buttons_style.buttonPressed,
                        ]}
                    >
                        <Text style={ticket_buttons_style.text}>Recargar</Text>
                    </Pressable>
                    <Pressable
                        onPress={handlePrintForPay}
                        style={({ pressed }) => [
                            ticket_buttons_style.baseButton,
                            pressed && ticket_buttons_style.buttonPressed,
                        ]}
                    >
                        <Text style={ticket_buttons_style.text}>
                            Remprimir Cobro
                        </Text>
                    </Pressable>
                </View>
            </SafeAreaView>
        </>
    );
}

import {
    Text,
    View,
    ScrollView,
    Pressable,
    Alert,
    ActivityIndicator,
    StyleSheet,
} from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import type { APIResponse, Ticket } from "types/api_types";
import { useState, useEffect } from "react";
import { useTicket } from "hooks/TicketContext";
import OrderRowView from "components/ticket/OrderRowView";
import BackButton from "components/BackButton";
import Constants from "expo-constants";
import { useAuth } from "hooks/AuthContext";

import { ticket_style, ticket_buttons_style } from "styles/ticket";
import TicketHeader from "components/ticket/TicketHeader";
import TicketMeta from "components/ticket/TicketMetaSection";
import { Ionicons, AntDesign } from "@expo/vector-icons";
import { TimerText } from "components/TimerText";
import DetailsMenu from "components/ticket/TicketDetailsMenu";

export default function TicketView() {
    const { uuid, isForPrinted } = useLocalSearchParams();
    const isForPrintedBool = isForPrinted === "true";
    const {
        ticket,
        payStoredTicket,
        refreshFromAPI,
        setTicket,
        initialized,
        setSyncingTicket,
    } = useTicket();

    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const [saveButton, setSaveButton] = useState(0);
    const [ticket_loading, setTicketLoading] = useState(true);
    const [ticketNotFound, setTicketNotFound] = useState(false);
    const [comments, setComments] = useState("");
    const [clientName, setClientName] = useState("");
    const { user, authFetch } = useAuth();
    const [trigger, setTrigger] = useState(0);
    const [menuVisible, setMenuVisible] = useState(false);

    function triggerFlush() {
        setTrigger(trigger + 1);
    }

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
        setSyncingTicket(true);
        await refreshFromAPI(ticket?.uuid).then(() => setSyncingTicket(false));
    }

    async function handlePrintForPay() {
        if (!ticket) return;
        triggerFlush();

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
        triggerFlush();

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
            <View
                style={{
                    flexDirection: "row",
                    justifyContent: "space-between",
                    alignItems: "center",
                    paddingHorizontal: 14,
                    marginVertical: 5,
                }}
            >
                <BackButton path="/" />
                <View
                    style={{
                        flexDirection: "row",
                        flex: 1,
                        justifyContent: "center",
                        alignItems: "center",
                    }}
                >
                    <Text style={ticket_style.tabText}>
                        Ticket #{ticket.ticket_number}
                        {" - "}
                        <TimerText timestamp={ticket.created_at} />
                    </Text>
                </View>
                <View
                    style={{
                        flexDirection: "row",
                        // minWidth: "50%",
                        flex: 1,
                        justifyContent: "space-around",
                        alignItems: "center",
                    }}
                >
                    {(user?.auth_level === "admin" ||
                        user?.auth_level === "manager") && (
                        <Pressable
                            onPress={handleDelete}
                            style={style.iconButton}
                        >
                            {/* <Text
                                style={[
                                    ticket_buttons_style.text,
                                    forms_style.deleteText,
                                ]}
                            >
                                Borrar
                            </Text> */}
                            <AntDesign
                                name="delete"
                                size={24}
                                color="#c62828"
                            />
                        </Pressable>
                    )}
                    <Pressable onPress={handleRefresh} style={style.iconButton}>
                        {/* <Text>Recargar</Text> */}
                        <Ionicons name="refresh" size={24} color="black" />
                    </Pressable>
                    {!isForPrintedBool && (
                        <Pressable
                            onPress={triggerFlush}
                            style={style.iconButton}
                        >
                            {/* <Text>Guardar</Text> */}
                            <Ionicons
                                name="save-outline"
                                size={24}
                                color="black"
                            />
                        </Pressable>
                    )}
                    <View>
                        <Pressable
                            onPress={() => setMenuVisible(!menuVisible)}
                            style={style.iconButton}
                        >
                            <Ionicons
                                name="ellipsis-vertical"
                                size={24}
                                color="#333"
                            />
                        </Pressable>
                        <DetailsMenu
                            menuVisible={menuVisible}
                            setMenuVisible={setMenuVisible}
                        />
                        {menuVisible && (
                            <Pressable
                                style={style.backdrop}
                                onPress={() => setMenuVisible(false)}
                            />
                        )}
                    </View>
                </View>
            </View>
            <View style={ticket_style.container}>
                <ScrollView>
                    <TicketHeader />
                    <TicketMeta
                        clientName={clientName}
                        setClientName={setClientName}
                        comments={comments}
                        setComments={setComments}
                        triggerFlush={trigger}
                    />
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
                                    <OrderRowView
                                        key={`order-row-${or.id}`}
                                        order={or}
                                        triggerToSend={saveButton}
                                    />
                                ))}
                        </View>
                    </View>
                </ScrollView>
                <View style={ticket_style.totalBar}>
                    <Text style={ticket_style.totalLabel}>Total</Text>
                    <Text style={ticket_style.totalValue}>${ticket_total}</Text>
                </View>
                <View style={ticket_buttons_style.footer}>
                    <View style={ticket_buttons_style.container}>
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

const style = StyleSheet.create({
    backdrop: {
        position: "absolute",
        top: 0,
        left: -1000,
        right: -1000,
        bottom: -1000,
        backgroundColor: "transparent",
        zIndex: 999,
    },
    iconButton: {
        padding: 8,
    },
});

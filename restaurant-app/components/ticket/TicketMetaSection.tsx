import { Text, View, TextInput } from "react-native";
import { useEffect, useRef, Dispatch, SetStateAction } from "react";
import { useTicket } from "hooks/TicketContext";

import { ticket_style } from "styles/ticket";

export interface Props {
    clientName: string;
    setClientName: Dispatch<SetStateAction<string>>;
    comments: string;
    setComments: Dispatch<SetStateAction<string>>;
    triggerFlush: number;
}

export default function TicketMeta({
    clientName,
    setClientName,
    comments,
    setComments,
    triggerFlush,
}: Props) {
    const {
        ticket,
        updateClientTicket,
        updateCommentsTicket,
        setSyncingTicket,
    } = useTicket();
    const commentsRef = useRef("");
    const hasHiddenTopComments =
        comments.trim().length > 0 &&
        (comments.startsWith("\n") || comments.split("\n").length > 3);

    useEffect(() => {
        flushTicket();
    }, [triggerFlush]);

    if (ticket === null) {
        return (
            <View style={ticket_style.headerContainer}>
                <Text style={ticket_style.headerText}>Cargando ...</Text>
            </View>
        );
    }

    async function handleClientChange() {
        if (ticket?.client_name === clientName) return;
        await updateClientTicket(clientName);
    }

    async function saveClientIfNeeded(force = false) {
        if (!ticket) return;

        if (!force && ticket.client_name === clientName) return;

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

    async function flushTicket(force = false) {
        setSyncingTicket(true);
        await saveClientIfNeeded(force);
        await saveCommentsIfNeeded(force);
        setSyncingTicket(false);
    }

    return (
        <View style={ticket_style.metaSection}>
            {ticket.restaurant_table.number === 0 && (
                <View style={ticket_style.clientContainer}>
                    <Text style={ticket_style.clientLabel}>Cliente</Text>
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
                <Text style={ticket_style.clientLabel}>Comentarios</Text>

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
    );
}

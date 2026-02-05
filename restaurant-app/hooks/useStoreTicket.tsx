import { useCallback, useEffect, useRef, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from "expo-router";
import { APIResponse, Ticket, newTicket, newOrder } from "types/api_types";
import Constants from "expo-constants";
import { useAuth } from "./AuthContext";

const STORAGE_KEY = "ticket";
const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;

export function useStoreTicket() {
    const [ticketState, setTicketState] = useState<Ticket | null>(null);
    const [initialized, setInitialized] = useState(false);
    const [syncing, setSyncing] = useState(false);
    const syncLock = useRef(false);
    const { authFetch } = useAuth();

    useEffect(() => {
        if (ticketState) {
            AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(ticketState));
        } else {
            AsyncStorage.removeItem(STORAGE_KEY);
        }
    }, [ticketState]);

    async function read(): Promise<Ticket | null> {
        try {
            const stored = await AsyncStorage.getItem(STORAGE_KEY);
            return stored ? (JSON.parse(stored) as Ticket) : null;
        } catch {
            return null;
        } finally {
            setInitialized(true);
        }
    }

    const save = useCallback((ticket: Ticket | null) => {
        setTicketState(ticket);
    }, []);

    function refreshFromStorage() {
        read().then(setTicketState);
    }

    useEffect(() => {
        refreshFromStorage();
    }, []);

    async function fetchTicketStable(uuid: string, retries = 4) {
        let lastTotal: number | null = null;

        for (let i = 0; i < retries; i++) {
            const res: APIResponse<Ticket> = await authFetch(
                API_URL +
                    "ticket/?filter_field=uuid&filter_value=" +
                    uuid +
                    "&relations=true&is_active=true",
                {
                    method: "GET",
                },
            ).then((r) => r.json());

            const ticket = res.response[0];

            if (ticket && ticket.total === lastTotal) {
                save(ticket);
                return;
            }

            lastTotal = ticket?.total ?? null;
            await new Promise((r) => setTimeout(r, 120));
        }

        const res: APIResponse<Ticket> = await authFetch(
            API_URL +
                "ticket/?filter_field=uuid&filter_value=" +
                uuid +
                "&relations=true&is_active=true",
            {
                method: "GET",
            },
        ).then((r) => r.json());

        save(res.response[0]);
    }

    async function sendStoredTicket() {
        if (!ticketState || syncLock.current) return;

        syncLock.current = true;
        setSyncing(true);

        const uuid = ticketState.uuid;
        const ticketId = ticketState.id;

        try {
            const payload: newTicket = {
                id_restaurant_table: ticketState.restaurant_table.id,
                comments: ticketState.comments,
                id_user: ticketState.id_user,
            };

            const ticketRes = await authFetch(API_URL + "ticket/" + ticketId, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!ticketRes.ok) {
                throw new Error(`Ticket update failed ${ticketRes.status}`);
            }

            for (const o of ticketState.orders) {
                if (o.quantity <= 0) continue;

                const orderPayload: newOrder = {
                    id: o.id,
                    quantity: o.quantity,
                    id_ticket: ticketId,
                    id_product: o.product.id,
                    order_addons: o.order_addons.map(
                        (oa) => oa.id_product_addons,
                    ),
                };

                const res = await authFetch(API_URL + "order/" + o.id, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(orderPayload),
                });

                if (!res.ok) {
                    throw new Error(`Order sync failed ${res.status}`);
                }
            }
        } catch (err) {
            console.log(String(err));
        } finally {
            await fetchTicketStable(uuid);
            syncLock.current = false;
            setSyncing(false);
        }
    }

    async function payStoredTicket() {
        if (!ticketState || syncLock.current) return;

        syncLock.current = true;
        setSyncing(true);

        try {
            console.log("pagando");
            const res = await authFetch(API_URL + "ticket/pay", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: ticketState.id,
                    is_paid: true,
                }),
            });

            if (!res.ok) {
                throw new Error(`Payment failed ${res.status}`);
            }

            save(null);
            router.replace("/orders/");
        } catch (err) {
            console.log(String(err));
        } finally {
            syncLock.current = false;
            setSyncing(false);
        }
    }

    async function removeOrder(orderId: number) {
        if (!ticketState || syncLock.current) return;

        syncLock.current = true;
        setSyncing(true);

        const uuid = ticketState.uuid;

        try {
            const res = await authFetch(API_URL + "order/" + orderId, {
                method: "DELETE",
            });

            if (!res.ok) {
                throw new Error(`Order delete failed ${res.status}`);
            }
        } catch (err) {
            console.log(String(err));
        } finally {
            await fetchTicketStable(uuid);
            syncLock.current = false;
            setSyncing(false);
        }
    }

    function setComments(comments: string) {
        if (!ticketState) return;

        setTicketState({
            ...ticketState,
            comments,
        });
    }

    async function updateClientTicket(client_name: string) {
        if (!ticketState || syncLock.current) return;

        syncLock.current = true;
        setSyncing(true);

        try {
            const res = await authFetch(API_URL + "ticket/client", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: ticketState.id,
                    client_name: client_name,
                }),
            });

            if (!res.ok) {
                throw new Error(`Client update failed ${res.status}`);
            }
            await fetchTicketStable(ticketState.uuid);
        } catch (err) {
            console.log(String(err));
        } finally {
            syncLock.current = false;
            setSyncing(false);
        }
    }

    async function updateCommentsTicket(comments: string) {
        if (!ticketState || syncLock.current || !comments) return;

        syncLock.current = true;
        setSyncing(true);

        try {
            const res = await authFetch(API_URL + "ticket/comments", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: ticketState.id,
                    comments: comments,
                }),
            });

            if (!res.ok) {
                throw new Error(`Comments update failed ${res.status}`);
            }
            await fetchTicketStable(ticketState.uuid);
        } catch (err) {
            console.log(String(err));
        } finally {
            syncLock.current = false;
            setSyncing(false);
        }
    }

    async function updateTableNumber(id_restaurant_table: number) {
        if (!ticketState || syncLock.current || !id_restaurant_table) return;

        syncLock.current = true;
        setSyncing(true);

        try {
            const res = await authFetch(API_URL + "ticket/table", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: ticketState.id,
                    id_restaurant_table: id_restaurant_table,
                }),
            });

            if (!res.ok) {
                throw new Error(`Table update failed ${res.status}`);
            }
            await fetchTicketStable(ticketState.uuid);
        } catch (err) {
            console.log(String(err));
        } finally {
            syncLock.current = false;
            setSyncing(false);
        }
    }

    const guarded = useCallback(
        <T extends (...args: any[]) => any>(fn: T) =>
            (...args: Parameters<T>) => {
                if (syncing) return;
                return fn(...args);
            },
        [syncing],
    );

    return {
        ticket: ticketState,
        syncingTicket: syncing,
        setSyncingTicket: setSyncing,
        initialized,
        setTicket: save,
        setComments,
        refreshFromStorage,
        refreshFromAPI: fetchTicketStable,
        sendStoredTicket: guarded(sendStoredTicket),
        payStoredTicket: guarded(payStoredTicket),
        removeOrder: guarded(removeOrder),
        updateClientTicket,
        updateCommentsTicket,
        updateTableNumber,
    };
}

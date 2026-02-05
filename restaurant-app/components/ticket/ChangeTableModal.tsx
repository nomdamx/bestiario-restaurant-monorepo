import { Modal, View, Text, Pressable, StyleSheet } from "react-native";
import { Dispatch, SetStateAction, useState, useEffect } from "react";
import { APIResponse, RestaurantTable } from "types/api_types";
import { useAuth } from "hooks/AuthContext";
import Constants from "expo-constants";
import DropdownTable from "./TableDropdown";
import { useTicket } from "hooks/TicketContext";

export interface Props {
    visible: boolean;
    setVisible: Dispatch<SetStateAction<boolean>>;
}

export default function ChangeTableModal({ visible, setVisible }: Props) {
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { updateTableNumber } = useTicket();
    const [tables, setTables] = useState<RestaurantTable[]>([]);
    const { user, loading, authFetch } = useAuth();
    const [selected, setSelected] = useState<RestaurantTable | null>(null);

    async function fetchTables() {
        try {
            const table_response: APIResponse<RestaurantTable> =
                await authFetch(API_URL + "restaurant-table?is_active=true", {
                    method: "GET",
                }).then((response) => response.json());
            setTables(table_response.response);
        } catch (error) {
            console.log(String(error));
        }
    }

    async function handleUpdateTable() {
        if (selected === null) return;
        await updateTableNumber(selected.id).then(() => setVisible(false));
    }

    useEffect(() => {
        if (loading) return;
        if (!user) return;

        fetchTables();
    }, [loading, user]);

    return (
        <Modal
            visible={visible}
            transparent={true}
            animationType="slide"
            onRequestClose={() => setVisible(false)}
        >
            <Pressable
                style={styles.backdrop}
                onPress={() => setVisible(false)}
            >
                <View style={styles.content}>
                    <Text style={styles.title}>Cambiar Mesa</Text>

                    <DropdownTable
                        selected={selected}
                        setSelected={setSelected}
                        tables={tables}
                    />

                    <Pressable
                        onPress={handleUpdateTable}
                        style={styles.changeButton}
                    >
                        <Text style={styles.text}>Cambiar</Text>
                    </Pressable>

                    <Pressable
                        style={styles.closeButton}
                        onPress={() => setVisible(false)}
                    >
                        <Text style={styles.text}>Cerrar</Text>
                    </Pressable>
                </View>
            </Pressable>
        </Modal>
    );
}

const styles = StyleSheet.create({
    backdrop: {
        flex: 1,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        justifyContent: "center",
        alignItems: "center",
    },
    content: {
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 24,
        width: "90%",
        maxWidth: 400,
    },
    title: {
        fontSize: 20,
        fontWeight: "600",
        marginBottom: 16,
    },
    changeButton: {
        marginTop: 20,
        padding: 12,
        backgroundColor: "#459b3f",
        borderRadius: 8,
        alignItems: "center",
    },
    closeButton: {
        marginTop: 10,
        padding: 12,
        backgroundColor: "#007AFF",
        borderRadius: 8,
        alignItems: "center",
    },
    text: {
        color: "#fff",
        fontWeight: "600",
    },
});

import { Modal, View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { useAuth } from "hooks/AuthContext";
import { useTicket } from "hooks/TicketContext";

export default function GlobalSyncModal() {
    const { loading } = useAuth();
    const { syncingTicket } = useTicket();

    return (
        <Modal
            visible={loading || syncingTicket}
            transparent={true}
            animationType="fade"
        >
            <View style={styles.backdrop}>
                <View style={styles.content}>
                    <ActivityIndicator size="large" color="#007AFF" />
                    <Text style={styles.text}>Sincronizando...</Text>
                </View>
            </View>
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
        padding: 32,
        alignItems: "center",
        minWidth: 200,
    },
    text: {
        marginTop: 16,
        fontSize: 16,
        color: "#333",
    },
});

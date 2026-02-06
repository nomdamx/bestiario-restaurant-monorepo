import { Text, Pressable, StyleSheet, FlatList } from "react-native";
import { Dispatch, SetStateAction, useState } from "react";
import { UserDropdown } from "types/api_types";

export interface Props {
    selected: string;
    setSelected: Dispatch<SetStateAction<string>>;
    setUser: Dispatch<SetStateAction<UserDropdown | null>>;
    users: UserDropdown[];
}

export default function DropdownUser({
    selected,
    setSelected,
    setUser,
    users,
}: Props) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <Pressable style={styles.button} onPress={() => setIsOpen(!isOpen)}>
                <Text style={styles.buttonText}>
                    {selected ? <>{selected}</> : "Selecciona un usuario"}
                </Text>
                <Text style={styles.arrow}>{isOpen ? "▲" : "▼"}</Text>
            </Pressable>

            {isOpen && (
                <FlatList
                    data={users}
                    keyExtractor={(item) => item.username}
                    style={styles.list}
                    renderItem={({ item }) => (
                        <Pressable
                            style={[
                                styles.item,
                                selected === item.username &&
                                    styles.selectedItem,
                            ]}
                            onPress={() => {
                                setSelected(item.username);
                                setUser(item);
                                setIsOpen(false);
                            }}
                        >
                            <Text
                                style={[
                                    styles.itemText,
                                    selected === item.username &&
                                        styles.selectedText,
                                ]}
                            >
                                {item.username}
                            </Text>
                            {selected === item.username && (
                                <Text style={styles.checkmark}>✓</Text>
                            )}
                        </Pressable>
                    )}
                />
            )}
        </>
    );
}

const styles = StyleSheet.create({
    button: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        padding: 14,
        backgroundColor: "#fff",
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        marginBottom: 8,
    },
    buttonText: {
        fontSize: 16,
        color: "#333",
        flex: 1,
    },
    arrow: {
        fontSize: 12,
        color: "#666",
        marginLeft: 8,
    },
    list: {
        maxHeight: 200,
        backgroundColor: "#fff",
        borderWidth: 1,
        borderColor: "#ddd",
        borderRadius: 8,
        marginBottom: 16,
        width: "100%",
    },
    item: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingVertical: 16,
        paddingHorizontal: 14,
        borderBottomWidth: 1,
        borderBottomColor: "#f0f0f0",
    },
    selectedItem: {
        backgroundColor: "#f0f8ff",
    },
    itemText: {
        fontSize: 18,
        color: "#333",
        flex: 1,
    },
    selectedText: {
        color: "#007AFF",
        fontWeight: "600",
    },
    checkmark: {
        fontSize: 20,
        color: "#007AFF",
        fontWeight: "bold",
        marginLeft: 8,
    },
});

import { Text, View, Pressable, StyleSheet } from "react-native";
import { Ionicons, Octicons } from "@expo/vector-icons";
import { Dispatch, SetStateAction, useState } from "react";
import ChangeTableModal from "./ChangeTableModal";

export interface Props {
    menuVisible: boolean;
    setMenuVisible: Dispatch<SetStateAction<boolean>>;
}
export default function DetailsMenu({ menuVisible, setMenuVisible }: Props) {
    const [modalVisible, setModalVisible] = useState(false);
    if (menuVisible) {
        return (
            <>
                <ChangeTableModal
                    visible={modalVisible}
                    setVisible={setModalVisible}
                />
                <View style={dropdownStyle.dropdown}>
                    <Pressable
                        style={dropdownStyle.menuItem}
                        onPress={() => {
                            setModalVisible(true);
                        }}
                    >
                        <Octicons name="number" size={20} color={"#333"} />
                        <Text style={dropdownStyle.menuText}>Cambiar Mesa</Text>
                    </Pressable>
                </View>
            </>
        );
    }
}

const dropdownStyle = StyleSheet.create({
    header: {
        position: "relative",
    },
    dropdown: {
        position: "absolute",
        top: 40,
        right: 0,
        backgroundColor: "#fff",
        borderRadius: 8,
        minWidth: 180,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 8,
        elevation: 5,
        paddingVertical: 8,
        zIndex: 1000,
    },
    menuItem: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 16,
        paddingVertical: 12,
        gap: 12,
    },
    menuText: {
        fontSize: 16,
        color: "#333",
    },
    backdrop: {
        position: "absolute",
        top: 0,
        left: -1000,
        right: -1000,
        bottom: -1000,
        backgroundColor: "transparent",
        zIndex: 999,
    },
});

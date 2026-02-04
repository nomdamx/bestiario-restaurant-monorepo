import { View, Text, Pressable, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import type { Href } from "expo-router";
import { useTicket } from "hooks/TicketContext";

export function NavBar() {
    const { ticket, setTicket } = useTicket();

    return (
        <View style={style.navbar}>
            <NavBarButton
                text="Inicio"
                path="/"
                onPress={() => setTicket(null)}
            />
            <NavBarButton text="Perfil" path="/profile" />
        </View>
    );
}

interface NavBarProps {
    text: string;
    path: Href;
    onPress?: () => void;
}

function NavBarButton({ text, path, onPress }: NavBarProps) {
    const router = useRouter();

    function handlePress() {
        if (onPress) {
            onPress();
        }
        router.push(path);
    }
    return (
        <Pressable
            onPress={handlePress}
            style={({ pressed }) => [
                style.button,
                pressed && style.buttonPressed,
            ]}
        >
            <Text style={style.buttonText}>{text}</Text>
        </Pressable>
    );
}

const style = StyleSheet.create({
    navbar: {
        flexDirection: "row",
        justifyContent: "space-around",
        alignItems: "center",
        width: "100%",
        padding: 20,
        backgroundColor: "#fff",
        position: "sticky",
        top: 0,
        zIndex: 50,

        borderWidth: 1,
        borderStyle: "solid",
        borderColor: "#ddd",
    },
    text: {
        fontSize: 18,
    },
    button: {
        paddingVertical: 10,
        paddingHorizontal: 20,
        borderRadius: 12,
        backgroundColor: "#e7e1e1ff",
    },
    buttonPressed: {
        backgroundColor: "#e0e0e0",
        transform: [{ scale: 0.97 }],
    },
    buttonText: {
        fontSize: 16,
        fontWeight: "500",
        color: "#333",
    },
});

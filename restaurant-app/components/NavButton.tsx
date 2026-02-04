import { Text, Pressable, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import type { Href } from "expo-router";

export interface Props {
    text: string;
    path: Href;
}

export function NavButton({ text, path }: Props) {
    const router = useRouter();

    return (
        <Pressable
            style={({ pressed }) => [
                style.button,
                pressed && style.buttonPressed,
            ]}
            onPress={() => router.push(path)}
        >
            <Text style={style.text}>{text}</Text>
        </Pressable>
    );
}
const style = StyleSheet.create({
    button: {
        width: "90%",
        backgroundColor: "#fff",
        alignItems: "center",
        borderRadius: 10,
        borderWidth: 1,
        borderColor: "#ddd",

        paddingVertical: 20,
        paddingHorizontal: 10,

        marginBottom: 10,

        // ios
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.12,
        shadowRadius: 18,

        // android
        elevation: 6,
    },
    buttonPressed: {
        transform: [{ scale: 0.98 }],
        backgroundColor: "#f5f5f5",
    },
    text: {
        fontSize: 24,
        fontWeight: "600",
        textAlign: "center",
    },
});

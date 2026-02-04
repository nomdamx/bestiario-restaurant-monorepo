import { NavButton } from "components/NavButton";
import { router } from "expo-router";
import { useAuth } from "hooks/AuthContext";
import { View, StyleSheet, Text, Pressable } from "react-native";

import { global_container_style } from "styles/global";

export default function HomeScreen() {
    const { user, loading, logout } = useAuth();
    if (loading) return null;

    const handleLogout = async () => {
        await logout();
        router.replace("/");
    };

    return (
        <View style={global_container_style.main_container}>
            {!user ? (
                <>
                    <NavButton text="Iniciar Sesion" path="/profile/login" />
                    <NavButton text="Registrarse" path="/profile/signup" />
                </>
            ) : (
                <View style={style.userContainer}>
                    <View style={style.header}>
                        <Text style={style.name}>{user.display_name}</Text>
                    </View>
                    <Pressable
                        onPress={handleLogout}
                        style={({ pressed }) => [
                            style.logoutButton,
                            pressed && style.logoutButtonPressed,
                        ]}
                    >
                        <Text style={style.logoutText}>Cerrar Sesion</Text>
                    </Pressable>
                </View>
            )}
        </View>
    );
}

const style = StyleSheet.create({
    userContainer: {
        alignItems: "center",
        gap: 16,
        flex: 1,
        justifyContent: "center",
    },
    header: {},
    name: {
        fontSize: 24,
        fontWeight: "600",
        color: "#333",
    },
    username: {
        fontSize: 18,
        fontWeight: "400",
        color: "#333",
    },
    logoutButton: {
        paddingVertical: 12,
        paddingHorizontal: 24,
        borderRadius: 12,
        backgroundColor: "#f0f0f0",
    },
    logoutButtonPressed: {
        backgroundColor: "#e0e0e0",
        transform: [{ scale: 0.97 }],
    },
    logoutText: {
        fontSize: 16,
        fontWeight: "500",
        color: "#333",
    },
});

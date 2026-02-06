import { NavButton } from "components/NavButton";
import { router } from "expo-router";
import { useAuth } from "hooks/AuthContext";
import { View, StyleSheet, Text, Pressable } from "react-native";
import { check_need_password, check_admin_see_config } from "hooks/auth_api";

import { global_container_style } from "styles/global";
import { useEffect, useState } from "react";
import Constants from "expo-constants";

export default function HomeScreen() {
    const { user, loading, logout, authFetch } = useAuth();
    const [needPassword, setNeedPassword] = useState<boolean>(true);
    const [adminConfig, setAdminConfig] = useState<boolean>(false);
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;

    async function handle_need_password() {
        const is_need = await check_need_password();
        setNeedPassword(is_need);
    }

    async function handle_admin_see_config() {
        const can_see = await check_admin_see_config();
        setAdminConfig(can_see);
    }

    async function handleChangeNeedPassword(value: boolean) {
        await authFetch(API_URL + "auth/user/need_password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ value: String(value) }),
        }).then(handle_need_password);
    }

    useEffect(() => {
        handle_need_password();
        handle_admin_see_config();
    }, []);

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

                    {(user?.auth_level === "admin" ||
                        user?.auth_level === "manager") &&
                        adminConfig && (
                            <View style={style.configContainer}>
                                <Text style={style.configTitle}>
                                    Configuración
                                </Text>
                                <View style={style.configOption}>
                                    <Text style={style.configLabel}>
                                        Requerir contraseña a usuarios
                                    </Text>
                                    <Pressable
                                        style={({ pressed }) => [
                                            style.logoutButton,
                                            pressed &&
                                                style.logoutButtonPressed,
                                        ]}
                                        onPress={() =>
                                            handleChangeNeedPassword(
                                                !needPassword,
                                            )
                                        }
                                    >
                                        <Text style={style.logoutText}>
                                            {needPassword ? "Sí" : "No"}
                                        </Text>
                                    </Pressable>
                                </View>
                            </View>
                        )}
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
    configContainer: {
        marginTop: 24,
        gap: 12,
        alignItems: "center",
    },
    configTitle: {
        fontSize: 18,
        fontWeight: "600",
        color: "#333",
    },
    configOption: {
        flexDirection: "row",
        alignItems: "center",
        gap: 12,
    },
    configLabel: {
        fontSize: 16,
        color: "#333",
    },
});

import { useEffect, useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet } from "react-native";
import { useAuth } from "hooks/AuthContext";
import { router } from "expo-router";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";
import { spacingHelpers } from "styles/tokens";
import DropdownUser from "components/auth/UserDropdown";
import Constants from "expo-constants";
import { UserDropdown } from "types/api_types";
import { check_need_password } from "hooks/auth_api";

export default function LoginScreen() {
    const { loginWithUser, user, loading, authFetch } = useAuth();
    const [username, setUsername] = useState("");
    const [logUser, setLogUser] = useState<UserDropdown | null>(null);
    const [needPassword, setNeedPassword] = useState<boolean>(true);
    const [password, setPassword] = useState("");
    const [users, setUsers] = useState<UserDropdown[]>([]);
    const [showPassword, setShowPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const [loadingUsers, setLoadingUsers] = useState(true);

    async function fetchUsers() {
        setLoadingUsers(true);
        try {
            const request = await authFetch(API_URL + "auth/user/", {
                method: "GET",
            }).then((response) => response.json());
            setUsers(request.response);
        } catch (error) {
            console.error("Error fetching users:", error);
        } finally {
            setLoadingUsers(false);
        }
    }

    async function handle_need_password() {
        const is_need = await check_need_password();
        setNeedPassword(is_need);
    }

    useEffect(() => {
        fetchUsers();
        handle_need_password();
    }, []);

    useEffect(() => {
        if (!loading && user) {
            router.replace("/");
        }
    }, [loading, user]);

    if (loading) return null;

    // const handleLogin = async () => {
    //     if (!username || (password && needPassword)) {
    //         setErrorMessage("Completa todos los campos");
    //         return;
    //     }
    //     setSubmitting(true);
    //     setErrorMessage(null);
    //     let success;
    //     try {
    //         if (!needPassword) {
    //             if (
    //                 (logUser?.auth_level === "admin" ||
    //                     logUser?.auth_level === "manager") &&
    //                 !password
    //             ) {
    //                 setErrorMessage("Completa todos los campos");
    //                 return;
    //             } else {
    //                 success = await loginWithUser(username, "false_password");
    //                 return;
    //             }
    //         }
    //         success = await loginWithUser(username, password);
    //     } catch {
    //         setErrorMessage("Error de conexión");
    //     } finally {
    //         if (!success) {
    //             setErrorMessage("Usuario o contraseña incorrectos");
    //         }
    //         setSubmitting(false);
    //     }
    // };
    const handleLogin = async () => {
        if (!username) {
            setErrorMessage("Selecciona un usuario");
            return;
        }

        setSubmitting(true);
        setErrorMessage(null);

        try {
            let success;

            if (!needPassword) {
                if (
                    logUser?.auth_level === "admin" ||
                    logUser?.auth_level === "manager"
                ) {
                    if (!password) {
                        setErrorMessage(
                            "Los administradores requieren contraseña",
                        );
                        setSubmitting(false);
                        return;
                    }
                    success = await loginWithUser(username, password);
                } else {
                    success = await loginWithUser(username, "false_password");
                }
            } else {
                if (!password) {
                    setErrorMessage("Completa todos los campos");
                    setSubmitting(false);
                    return;
                }
                success = await loginWithUser(username, password);
            }

            if (!success) {
                setErrorMessage("Usuario o contraseña incorrectos");
            }
        } catch {
            setErrorMessage("Error de conexión");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <View
            style={[
                global_container_style.main_container,
                { gap: spacingHelpers.section },
            ]}
        >
            <Text style={forms_style.title}>Iniciar Sesion</Text>

            {/* <TextInput
                style={forms_style.input}
                placeholder="Username"
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
            /> */}
            {loadingUsers ? (
                <Text>Cargando usuarios...</Text>
            ) : (
                <DropdownUser
                    selected={username}
                    setSelected={setUsername}
                    setUser={setLogUser}
                    users={users}
                />
            )}
            {(logUser?.auth_level === "admin" ||
                logUser?.auth_level === "manager") && (
                <View style={forms_style.passwordContainer}>
                    <TextInput
                        style={[forms_style.input, { flex: 1 }]}
                        placeholder="Password"
                        value={password}
                        onChangeText={setPassword}
                        secureTextEntry={!showPassword}
                    />
                    <Pressable
                        onPress={() => setShowPassword(!showPassword)}
                        style={forms_style.showButton}
                    >
                        <Text style={forms_style.showButtonText}>
                            {showPassword ? "Ocultar" : "Mostrar"}
                        </Text>
                    </Pressable>
                </View>
            )}

            {errorMessage && (
                <Text style={forms_style.error}>{errorMessage}</Text>
            )}

            <Pressable
                onPress={handleLogin}
                style={({ pressed }) => [
                    forms_style.backButton,
                    (pressed || submitting) && forms_style.pressedEffect,
                ]}
                disabled={submitting}
            >
                <Text style={forms_style.backButtonText}>
                    {submitting ? "Ingresando..." : "Continue"}
                </Text>
            </Pressable>
        </View>
    );
}

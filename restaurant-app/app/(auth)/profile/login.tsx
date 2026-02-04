import { useEffect, useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet } from "react-native";
import { useAuth } from "hooks/AuthContext";
import { router } from "expo-router";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";
import { spacingHelpers } from "styles/tokens";

export default function LoginScreen() {
    const { loginWithUser, user, loading } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        if (!loading && user) {
            router.replace("/");
        }
    }, [loading, user]);

    if (loading) return null;

    const handleLogin = async () => {
        if (!username || !password) {
            setErrorMessage("Completa todos los campos");
            return;
        }
        setSubmitting(true);
        setErrorMessage(null);

        try {
            const success = await loginWithUser(username, password);
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

            <TextInput
                style={forms_style.input}
                placeholder="Username"
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
            />

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

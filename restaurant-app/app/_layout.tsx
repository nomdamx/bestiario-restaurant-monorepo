import { Stack } from "expo-router";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { TicketProvider } from "hooks/TicketContext";
import { AuthProvider, useAuth } from "hooks/AuthContext";
import { colors } from "styles/tokens";

export default function RootLayout() {
    return (
        <SafeAreaProvider>
            <AuthProvider>
                <AuthGate />
            </AuthProvider>
        </SafeAreaProvider>
    );
}

function AuthGate() {
    const { loading } = useAuth();

    if (loading) {
        return null;
    }

    return (
        <TicketProvider>
            <Stack
                screenOptions={{
                    headerShown: false,
                    animation: "none",
                    contentStyle: { backgroundColor: colors.background },
                }}
            />
        </TicketProvider>
    );
}

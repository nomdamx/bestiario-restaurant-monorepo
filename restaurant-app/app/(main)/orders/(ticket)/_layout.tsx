import { Stack } from "expo-router";
import { colors } from "styles/tokens";
import { SafeAreaProvider } from "react-native-safe-area-context";

export default function TicketLayout() {
    return (
        <SafeAreaProvider>
            <Stack
                screenOptions={{
                    headerShown: false,
                    animation: "none",
                    contentStyle: { backgroundColor: colors.background },
                }}
            />
        </SafeAreaProvider>
    );
}

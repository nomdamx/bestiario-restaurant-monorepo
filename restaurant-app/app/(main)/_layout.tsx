import { SafeAreaView } from "react-native-safe-area-context";
import { Slot, router } from "expo-router";
import { ActivityIndicator } from "react-native";
import { NavBar } from "components/NavBar";
import { useAuth } from "hooks/AuthContext";
import { useEffect, useState } from "react";

import { global_container_style } from "styles/global";

export default function AppLayout() {
    const { user, loading } = useAuth();

    const [redirecting, setRedirecting] = useState(false);

    useEffect(() => {
        if (!loading && !user) {
            setRedirecting(true);
            router.replace("/profile");
        }
    }, [loading, user]);

    if (loading || redirecting) {
        return (
            <SafeAreaView style={{ flex: 1, justifyContent: "center" }}>
                <ActivityIndicator />
            </SafeAreaView>
        );
    }

    return (
        <SafeAreaView style={global_container_style.layout_container}>
            <Slot />
            <NavBar />
        </SafeAreaView>
    );
}

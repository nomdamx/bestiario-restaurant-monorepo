import { SafeAreaView } from "react-native-safe-area-context";
import { Slot } from "expo-router";
import { NavBar } from "components/NavBar";

import { global_container_style } from "styles/global";

export default function AuthLayout() {
    return (
        <SafeAreaView style={global_container_style.layout_container}>
            <Slot />
            <NavBar />
        </SafeAreaView>
    );
}

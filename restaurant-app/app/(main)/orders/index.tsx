import { View, Pressable, Text } from "react-native";
import { NavButton } from "components/NavButton";
import { router } from "expo-router";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";

export default function Orders() {
    return (
        <>
            <Pressable
                onPress={() => router.replace("/")}
                style={({ pressed }) => [
                    global_container_style.backButton,
                    pressed && forms_style.pressedEffect,
                ]}
            >
                <Text style={global_container_style.backButtonText}>
                    Regresar
                </Text>
            </Pressable>
            <View style={global_container_style.main_container}>
                <NavButton text="Nuevos Pedidos" path="/orders/new" />
                <NavButton
                    text="Pedidos Activos"
                    path="/orders/active_tables"
                />
                <NavButton text="Pedidos Impresos" path="/orders/old" />
            </View>
        </>
    );
}

import { Text, Pressable } from "react-native";
import { router } from "expo-router";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";
import type { Href } from "expo-router";
import { Ionicons, AntDesign } from "@expo/vector-icons";

export interface Props {
    path: Href;
}

export default function BackButton({ path }: Props) {
    return (
        <Pressable
            onPress={() => router.replace(path)}
            // style={({ pressed }) => [
            //     global_container_style.backButton,
            //     pressed && forms_style.pressedEffect,
            // ]}
        >
            {/* <Text style={global_container_style.backButtonText}>Regresar</Text> */}
            <Ionicons name="arrow-back" size={24} color="black" />
        </Pressable>
    );
}

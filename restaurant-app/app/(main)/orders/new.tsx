import { FlatList, Pressable, Text } from "react-native";
import { useState, useEffect } from "react";
import { APIResponse, RestaurantTable } from "types/api_types";
import { TableCard } from "components/TableCard";
import Constants from "expo-constants";
import { router } from "expo-router";
import { useAuth } from "hooks/AuthContext";

import { global_container_style } from "styles/global";
import { forms_style } from "styles/forms";

export default function OrdersNew() {
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const [tables, setTables] = useState<RestaurantTable[]>([]);
    const { user, loading, authFetch } = useAuth();

    useEffect(() => {
        if (loading) return;
        if (!user) return;

        fetchTables();
    }, [loading, user]);

    if (loading) {
        return <Text>Cargando...</Text>;
    }

    if (!user) {
        return <Text>No autenticado</Text>;
    }

    function sortTables(tables: RestaurantTable[]) {
        return [...tables]
            .filter((table) => table.number !== 0)
            .sort((a, b) => {
                return a.number - b.number;
            });
    }

    async function fetchTables() {
        try {
            const table_response: APIResponse<RestaurantTable> =
                await authFetch(API_URL + "restaurant-table?is_active=true", {
                    method: "GET",
                }).then((response) => response.json());
            setTables(table_response.response);
        } catch (error) {
            console.log(String(error));
        }
    }

    return (
        <>
            <Pressable
                onPress={() => router.push("/orders/")}
                style={({ pressed }) => [
                    global_container_style.backButton,
                    pressed && forms_style.pressedEffect,
                ]}
            >
                <Text style={global_container_style.backButtonText}>
                    Regresar
                </Text>
            </Pressable>
            <FlatList
                data={sortTables(tables)}
                numColumns={2}
                keyExtractor={(item, idx) => "table-" + idx}
                renderItem={({ item }) => (
                    <TableCard table={item} user={user} loading={loading} />
                )}
                contentContainerStyle={global_container_style.gridContainer}
                columnWrapperStyle={global_container_style.columnWrapper}
            />
        </>
    );
}

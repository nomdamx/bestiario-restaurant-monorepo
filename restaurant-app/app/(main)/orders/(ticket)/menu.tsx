import { View, FlatList, Pressable, Text, TextInput } from "react-native";
import { useState, useEffect, useMemo, useReducer, useCallback } from "react";
import { useTicket } from "hooks/TicketContext";
import { APIResponse, Category, ProductAddons } from "types/api_types";
import { CategoryCard } from "components/CategoryCard";
import { router } from "expo-router";
import Constants from "expo-constants";
import { useSendOrder } from "hooks/useSendOrder";

import { global_container_style } from "styles/global";
import { forms_style, menu_style } from "styles/forms";
import { useAuth } from "hooks/AuthContext";

type ProductState = {
    quantity: number;
    addons: number[];
};

type Action = {
    type: "update";
    productId: number;
    updater: (prev: ProductState) => ProductState;
};

function productReducer(state: Record<number, ProductState>, action: Action) {
    switch (action.type) {
        case "update": {
            const prev = state[action.productId];
            const next = action.updater(prev);

            if (prev === next) return state;

            return {
                ...state,
                [action.productId]: next,
            };
        }
        default:
            return state;
    }
}

export default function MenuView() {
    const API_URL = Constants.expoConfig?.extra?.flaskApiUrl;
    const { ticket, refreshFromAPI } = useTicket();
    const [categories, setCategories] = useState<Category[]>([]);
    const [addons, setAddons] = useState<ProductAddons[]>([]);
    const [search, setSearch] = useState("");
    const [productState, dispatch] = useReducer(productReducer, {});
    const [trigger, setTrigger] = useState(0);
    const { sendOrder } = useSendOrder();
    const { authFetch } = useAuth();

    async function fetchMenu() {
        try {
            const api_respone: APIResponse<Category> = await authFetch(
                API_URL + "category?relations=true&is_active=true",
                {
                    method: "GET",
                },
            ).then((response) => response.json());
            setCategories(api_respone.response);
        } catch (error) {
            console.log(String(error));
        }
    }

    async function fetchAddons() {
        try {
            const api_respone: APIResponse<ProductAddons> = await authFetch(
                API_URL + "product-addons?is_active=true",
                {
                    method: "GET",
                },
            ).then((response) => response.json());
            setAddons(api_respone.response);
        } catch (error) {
            console.log(String(error));
        }
    }

    async function handleRefresh() {
        if (!ticket) return;
        await refreshFromAPI(ticket?.uuid);
    }

    async function handleBack() {
        await handleRefresh().then(() => router.back());
    }

    useEffect(() => {
        fetchMenu();
        fetchAddons();
    }, []);

    function handleAdd() {
        if (!ticket) return;

        Object.entries(productState).forEach(([productId, state]) => {
            if (state.quantity <= 0) return;

            sendOrder({
                id_product: Number(productId),
                quantity: state.quantity,
                id_ticket: ticket.id,
                order_addons: state.addons,
            });
        });
        handleBack();
    }

    const updateProductState = useCallback(
        (productId: number, updater: (prev: ProductState) => ProductState) => {
            dispatch({ type: "update", productId, updater });
        },
        [],
    );

    const filteredCategories: Category[] = useMemo(() => {
        if (!search.trim()) return categories;

        const q = search.toLowerCase();

        return categories
            .map((category) => {
                const categoryMatch = category.name.toLowerCase().includes(q);

                const products = category.products ?? [];

                const filteredProducts = products.filter(
                    (product) =>
                        product.name.toLowerCase().includes(q) ||
                        product.complete_name.toLowerCase().includes(q) ||
                        product.ingredient_description
                            ?.toLowerCase()
                            .includes(q),
                );

                if (categoryMatch || filteredProducts.length > 0) {
                    return {
                        ...category,
                        products: categoryMatch ? products : filteredProducts,
                    };
                }

                return null;
            })
            .filter((c): c is Category => c !== null);
    }, [categories, search]);

    const getProductState = useCallback(
        (productId: number) => productState[productId],
        [productState],
    );

    return (
        <>
            <View style={menu_style.headerContainer}>
                <Pressable
                    onPress={handleBack}
                    style={({ pressed }) => [
                        global_container_style.backButton,
                        pressed && forms_style.pressedEffect,
                    ]}
                >
                    <Text style={global_container_style.backButtonText}>
                        {ticket ? "Regresar al Ticket" : "Regresar"}
                    </Text>
                </Pressable>
                <TextInput
                    value={search}
                    onChangeText={setSearch}
                    placeholder="Buscar por categoría o producto..."
                    placeholderTextColor="#999"
                    style={menu_style.searchInput}
                    clearButtonMode="while-editing"
                />
            </View>
            <FlatList
                data={filteredCategories}
                numColumns={1}
                keyExtractor={(item) => String(item.id)}
                removeClippedSubviews
                initialNumToRender={4}
                windowSize={7}
                maxToRenderPerBatch={5}
                renderItem={({ item }) => (
                    <CategoryCard
                        category={item}
                        addons={addons}
                        getProductState={getProductState}
                        updateProductState={updateProductState}
                        triggerToSend={trigger}
                    />
                )}
                contentContainerStyle={global_container_style.gridContainer}
            />
            {ticket && (
                <View style={menu_style.footerContainer}>
                    <Pressable
                        style={({ pressed }) => [
                            menu_style.secondaryButton,
                            pressed && forms_style.pressedEffect,
                        ]}
                        onPress={handleBack}
                    >
                        <Text style={menu_style.secondaryButtonText}>
                            Cancelar
                        </Text>
                    </Pressable>

                    <Pressable
                        style={({ pressed }) => [
                            menu_style.addButton,
                            pressed && forms_style.pressedEffect,
                        ]}
                        onPress={handleAdd}
                    >
                        <Text style={menu_style.addButtonText}>
                            Añadir al Ticket
                        </Text>
                    </Pressable>
                </View>
            )}
        </>
    );
}

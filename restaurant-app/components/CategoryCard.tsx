import { Pressable, Text, StyleSheet, View } from "react-native";
import { Category, ProductAddons } from "types/api_types";
import { ProductCard } from "./ProductCard";
import { router } from "expo-router";
import { useState, useEffect, useMemo, useCallback } from "react";
import { ProductCardMenu } from "./ProductMenu";

type ProductState = {
    quantity: number;
    addons: number[];
};

export interface Props {
    category: Category;
    addons: ProductAddons[];
    triggerToSend: number;
    getProductState: (productId: number) => ProductState | undefined;
    updateProductState: (
        productId: number,
        updater: (prev: ProductState) => ProductState,
    ) => void;
}

type AddonGroups = {
    [type: string]: {
        [price: string]: ProductAddons[];
    };
};

export function CategoryCard({
    category,
    addons,
    getProductState,
    updateProductState,
    triggerToSend,
}: Props) {
    const addonsGroup = useMemo<AddonGroups>(() => {
        const group: AddonGroups = {};

        addons.forEach((addon) => {
            const type = addon.type ?? "other";
            const price = String(addon.price);

            if (!group[type]) group[type] = {};
            if (!group[type][price]) group[type][price] = [];

            group[type][price].push(addon);
        });

        return group;
    }, [addons]);

    const makeUpdateState = useCallback(
        (productId: number) => (fn: (prev: ProductState) => ProductState) =>
            updateProductState(productId, fn),
        [updateProductState],
    );

    return (
        <View style={style.card}>
            <Text style={style.title}>{category.name}</Text>

            {category.ingredient_description && (
                <Text style={style.description}>
                    {category.ingredient_description}
                </Text>
            )}

            {category.products?.length === 0 && (
                <Text style={style.empty}>No hay productos</Text>
            )}

            {category.products?.map((p) => (
                <ProductCardMenu
                    key={p.id}
                    product={p}
                    grouped_addons={addonsGroup}
                    state={getProductState(p.id)}
                    updateState={makeUpdateState(p.id)}
                    triggerToSend={triggerToSend}
                />
            ))}
        </View>
    );
}
const style = StyleSheet.create({
    card: {
        backgroundColor: "#ffffff",
        borderRadius: 14,
        padding: 16,
        marginBottom: 16,

        shadowColor: "#000",
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.08,
        shadowRadius: 8,
        elevation: 4,
    },

    title: {
        fontSize: 18,
        fontWeight: "700",
        color: "#333",
        marginBottom: 6,
    },

    description: {
        fontSize: 14,
        color: "#666",
        marginBottom: 10,
    },

    empty: {
        fontSize: 14,
        color: "#999",
        marginVertical: 6,
    },
});

const styleAddons = StyleSheet.create({
    container: {
        marginTop: 12,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: "#f0f0f0",
    },

    typeGroup: {
        marginBottom: 12,
    },

    typeHeader: {
        fontSize: 15,
        fontWeight: "700",
        color: "#555",
        marginBottom: 6,
    },

    priceGroup: {
        flexDirection: "row",
        flexWrap: "wrap",
        alignItems: "baseline",
        marginBottom: 4,
    },

    addonText: {
        flexShrink: 1,
        fontSize: 12,
        color: "#555",
        lineHeight: 20,
    },

    priceText: {
        fontSize: 12,
        fontWeight: "600",
        color: "#4CAF50",
        marginLeft: 6,
    },
});

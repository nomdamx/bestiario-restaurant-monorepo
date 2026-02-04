import { useSendOrder } from "hooks/useSendOrder";
import { useTicket } from "hooks/TicketContext";
import React, { useEffect, useState } from "react";
import { View, Pressable, Text, StyleSheet } from "react-native";
import { Product, ProductAddons } from "types/api_types";

type AddonGroups = {
    [type: string]: {
        [price: string]: ProductAddons[];
    };
};

const DEFAULT_PRODUCT_STATE = {
    quantity: 0,
    addons: [],
};

export interface Props {
    product: Product;
    triggerToSend?: number;
    grouped_addons: AddonGroups;
    state?: {
        quantity: number;
        addons: number[];
    };
    updateState: (
        fn: (prev: { quantity: number; addons: number[] }) => {
            quantity: number;
            addons: number[];
        },
    ) => void;
}

function areEqual(prev: Props, next: Props) {
    return (
        prev.product.id === next.product.id &&
        prev.state?.quantity === next.state?.quantity &&
        prev.state?.addons === next.state?.addons &&
        prev.triggerToSend === next.triggerToSend
    );
}
export const ProductCardMenu = React.memo(function ProductCardMenu({
    product,
    triggerToSend,
    grouped_addons,
    state,
    updateState,
}: Props) {
    const { ticket } = useTicket();
    const { sendOrder } = useSendOrder();
    const [showAddons, setShowAddons] = useState(false);

    const quantity = state?.quantity ?? 0;
    const selectedAddons = state?.addons ?? [];

    function addOne() {
        updateState((prev = DEFAULT_PRODUCT_STATE) => ({
            ...prev,
            quantity: prev.quantity + 1,
        }));
    }

    function minusOne() {
        updateState((prev = DEFAULT_PRODUCT_STATE) => {
            const nextQty = Math.max(0, prev.quantity - 1);
            if (nextQty === prev.quantity) return prev;
            return { ...prev, quantity: nextQty };
        });
    }

    function toggleAddon(id: number) {
        updateState((prev = DEFAULT_PRODUCT_STATE) => {
            const exists = prev.addons.includes(id);

            const nextAddons = exists
                ? prev.addons.filter((a) => a !== id)
                : [...prev.addons, id];

            if (exists && nextAddons.length === prev.addons.length) {
                return prev;
            }

            return {
                ...prev,
                addons: nextAddons,
            };
        });
    }

    function isSelected(id: number) {
        return selectedAddons.includes(id);
    }

    function textForAddonsType(addon_type: string) {
        if (addon_type === "outside") return "Especialidades por Fuera";
        return "";
    }

    useEffect(() => {
        if (!ticket || !triggerToSend || quantity <= 0) return;

        sendOrder({
            id_product: product.id,
            quantity,
            id_ticket: ticket.id,
            order_addons: selectedAddons,
        });
    }, [triggerToSend]);

    return (
        <View style={style.container}>
            <View style={style.cardInfo}>
                <View style={style.productTextGroup}>
                    <View>
                        <Text
                            style={style.textName}
                            numberOfLines={2}
                            ellipsizeMode="tail"
                        >
                            {product.name}
                        </Text>
                        <Text style={style.textDescription}>
                            {product.ingredient_description}
                        </Text>
                    </View>
                    <Text style={style.textPrice}>${product.price}</Text>
                </View>
                {ticket && (
                    <View style={style.quantityContainer}>
                        <Pressable
                            onPress={minusOne}
                            style={({ pressed }) => [
                                style.quantityButton,
                                pressed && style.pressedScale,
                            ]}
                        >
                            <Text style={style.quantityButtonText}>-</Text>
                        </Pressable>

                        <Text style={style.quantityText}>{quantity}</Text>

                        <Pressable
                            onPress={addOne}
                            style={({ pressed }) => [
                                style.quantityButton,
                                pressed && style.pressedScale,
                            ]}
                        >
                            <Text style={style.quantityButtonText}>+</Text>
                        </Pressable>
                    </View>
                )}
            </View>

            {Object.keys(grouped_addons).length > 0 && (
                <View style={styleAddons.container}>
                    <Pressable
                        onPress={() => setShowAddons((v) => !v)}
                        style={({ pressed }) => [
                            {
                                alignSelf: "flex-start",
                                paddingVertical: 6,
                                paddingHorizontal: 10,
                                borderRadius: 8,
                                backgroundColor: "#f3f3f3",
                                marginBottom: showAddons ? 10 : 0,
                            },
                            pressed && { opacity: 0.8 },
                        ]}
                    >
                        <Text
                            style={{
                                fontSize: 13,
                                fontWeight: "600",
                                color: "#333",
                            }}
                        >
                            {showAddons
                                ? "Ocultar especialidades"
                                : "Mostrar especialidades"}
                        </Text>
                    </Pressable>

                    {showAddons &&
                        Object.entries(grouped_addons).map(([type, prices]) => (
                            <View key={type} style={styleAddons.typeGroup}>
                                <Text style={styleAddons.typeHeader}>
                                    {textForAddonsType(type)}
                                </Text>

                                {Object.entries(prices).map(
                                    ([price, addons]) => (
                                        <View
                                            key={type + "-" + price}
                                            style={styleAddons.priceGroup}
                                        >
                                            <View
                                                style={
                                                    styleAddons.addons_container
                                                }
                                            >
                                                {addons.map((addon) => {
                                                    const selected = isSelected(
                                                        addon.id,
                                                    );
                                                    return (
                                                        <Pressable
                                                            key={addon.id}
                                                            onPress={() =>
                                                                toggleAddon(
                                                                    addon.id,
                                                                )
                                                            }
                                                            style={({
                                                                pressed,
                                                            }) => [
                                                                styleAddons.addons_pressable,
                                                                {
                                                                    borderColor:
                                                                        selected
                                                                            ? "#4CAF50"
                                                                            : "#ccc",
                                                                    backgroundColor:
                                                                        selected
                                                                            ? "#e8f8ee"
                                                                            : "#ffffff",
                                                                },
                                                                pressed && {
                                                                    transform: [
                                                                        {
                                                                            scale: 0.97,
                                                                        },
                                                                    ],
                                                                    opacity: 0.85,
                                                                },
                                                            ]}
                                                        >
                                                            <Text
                                                                style={[
                                                                    styleAddons.addonText,
                                                                    {
                                                                        fontWeight:
                                                                            selected
                                                                                ? "700"
                                                                                : "500",
                                                                        color: selected
                                                                            ? "#2e7d32"
                                                                            : "#444",
                                                                    },
                                                                ]}
                                                            >
                                                                {addon.name}
                                                            </Text>
                                                        </Pressable>
                                                    );
                                                })}
                                            </View>

                                            <Text style={styleAddons.priceText}>
                                                +${price}
                                            </Text>
                                        </View>
                                    ),
                                )}
                            </View>
                        ))}
                </View>
            )}
        </View>
    );
}, areEqual);

const style = StyleSheet.create({
    container: {
        backgroundColor: "#fafafa",
        paddingVertical: 12,
        paddingHorizontal: 12,
        borderRadius: 10,

        borderWidth: 1,
        borderColor: "#eee",

        marginBottom: 10,
    },

    cardInfo: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        marginBottom: 12,
    },

    productTextGroup: {
        flex: 1,
        marginRight: 12,
        minWidth: 0,
    },

    textName: {
        fontSize: 16,
        fontWeight: "600",
        color: "#333",
        lineHeight: 22,

        flexShrink: 1,
    },
    textDescription: {
        fontSize: 12,
        fontWeight: "400",
        color: "#333",
        lineHeight: 22,

        flexShrink: 1,
    },

    textPrice: {
        fontSize: 18,
        fontWeight: "700",
        color: "#4CAF50",
        marginTop: 2,
    },

    quantityContainer: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#f2f2f2",
        borderRadius: 10,
        paddingHorizontal: 10,
        paddingVertical: 8,
        minWidth: 96,
        justifyContent: "space-between",
    },

    quantityButton: {
        width: 50,
        height: 50,
        borderRadius: 8,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#ffffff",

        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.08,
        shadowRadius: 2,
        elevation: 1,
    },

    quantityButtonText: {
        fontSize: 20,
        fontWeight: "700",
        color: "#333",
        lineHeight: 20,
    },

    quantityText: {
        fontSize: 20,
        fontWeight: "700",
        color: "#333",
        marginHorizontal: 6,
        minWidth: 20,
        textAlign: "center",
    },

    addonsContainer: {
        marginTop: 10,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: "#f0f0f0",
        flexDirection: "row",
        flexWrap: "wrap",
    },

    addonItem: {
        paddingVertical: 6,
        paddingHorizontal: 10,
        backgroundColor: "#f9f9f9",
        borderRadius: 8,
        borderWidth: 1,
        borderColor: "#ddd",
        marginRight: 6,
        marginBottom: 6,
        maxWidth: "100%",
    },

    addonItemText: {
        fontSize: 13,
        fontWeight: "500",
        color: "#555",
    },

    addonItemSelected: {
        borderColor: "#4CAF50",
        backgroundColor: "#e8f8ee",
    },

    pressedScale: {
        transform: [{ scale: 0.97 }],
        opacity: 0.85,
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
    addons_container: {
        flexDirection: "row",
        flexWrap: "wrap",
        marginTop: 6,
    },
    addons_pressable: {
        paddingHorizontal: 10,
        paddingVertical: 5,
        borderRadius: 999,
        borderWidth: 1,
        marginRight: 6,
        marginBottom: 6,
    },
});

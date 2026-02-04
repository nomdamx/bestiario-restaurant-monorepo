import { useSendOrder } from "hooks/useSendOrder";
import { useTicket } from "hooks/TicketContext";
import { useEffect, useState } from "react";
import { View, Pressable, Text, StyleSheet } from "react-native";
import { Product, ProductAddons, newOrder } from "types/api_types";

export interface Props {
    product: Product;
    isEditable?: boolean;
    triggerToSend?: number;
    product_addons?: ProductAddons[];
}

type AddonGroups = {
    [type: string]: {
        [price: string]: ProductAddons[];
    };
};

export function ProductCard({
    product,
    isEditable,
    triggerToSend,
    product_addons,
}: Props) {
    const { ticket } = useTicket();
    const [new_order, setNewOrder] = useState<newOrder | null>(null);
    const [selectedAddons, setSelectedAddons] = useState<number[]>([]);
    const [newQuantity, setNewQuantity] = useState(0);
    const { sendOrder } = useSendOrder();
    const [addonsGroup, setAddonsGroup] = useState<AddonGroups>({});
    const [showAddons, setShowAddons] = useState(false);

    function groupAddons(addons: ProductAddons[]) {
        const group: AddonGroups = {};

        addons.forEach((addon) => {
            const type = addon.type ?? "other";
            const price = String(addon.price);

            if (!group[type]) group[type] = {};

            if (!group[type][price]) group[type][price] = [];

            group[type][price].push(addon);
        });
        setAddonsGroup(group);
    }

    useEffect(() => {
        if (!product_addons || product_addons.length === 0) {
            setAddonsGroup({});
            return;
        }

        groupAddons(product_addons);
    }, [product_addons]);

    function addOne() {
        setNewQuantity(newQuantity + 1);
    }

    function minusOne() {
        if (newQuantity > 0) setNewQuantity(newQuantity - 1);
    }

    function isSelected(id: number) {
        return selectedAddons.includes(id);
    }

    const toggleAddon = (id: number) => {
        setSelectedAddons((prev) =>
            prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id],
        );
    };

    function textForAddonsType(addon_type: string) {
        if (addon_type === "outside") return "Especialidades por Fuera";
    }

    useEffect(() => {
        if (newQuantity > 0 && ticket) {
            const updated: newOrder = {
                id_product: product.id,
                quantity: newQuantity,
                id_ticket: ticket.id,
                order_addons: selectedAddons,
            };
            setNewOrder(updated);
        }
    }, [newQuantity, selectedAddons]);

    useEffect(() => {
        if (!ticket) return;
        sendOrder(new_order);
    }, [triggerToSend]);

    if (!isEditable) {
        return (
            <View style={style.container}>
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
        );
    }

    return (
        <View style={style.containerEditable}>
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
                {isEditable && (
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
                        <Text style={style.quantityText}>{newQuantity}</Text>
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
            {Object.keys(addonsGroup).length > 0 && (
                <View style={styleAddons.container}>
                    {/* Botón mostrar / ocultar */}
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

                    {/* Contenido */}
                    {showAddons &&
                        Object.entries(addonsGroup).map(([type, prices]) => (
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
                                                style={{
                                                    flexDirection: "row",
                                                    flexWrap: "wrap",
                                                    flex: 1,
                                                }}
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
                                                                {
                                                                    paddingHorizontal: 10,
                                                                    paddingVertical: 6,
                                                                    borderRadius: 10,
                                                                    borderWidth: 1,
                                                                    borderColor:
                                                                        selected
                                                                            ? "#4CAF50"
                                                                            : "#ccc",
                                                                    backgroundColor:
                                                                        selected
                                                                            ? "#e8f8ee"
                                                                            : "#ffffff",
                                                                    marginRight: 8,
                                                                    marginBottom: 6,
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
                                                                        fontSize: 13,
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
}
const style = StyleSheet.create({
    container: {
        flexDirection: "row",
        backgroundColor: "#ffffff",
        justifyContent: "space-between",
        alignSelf: "stretch",
        marginBottom: 10,
        padding: 8,
        borderTopWidth: 1,
        borderTopColor: "#ccc",
    },

    containerEditable: {
        backgroundColor: "#ffffff",
        alignSelf: "stretch",
        marginBottom: 16,
        borderRadius: 14,
        padding: 16,

        shadowColor: "#000",
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.08,
        shadowRadius: 10,
        elevation: 4,
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
        paddingHorizontal: 6,
        paddingVertical: 4,
        minWidth: 96,
        justifyContent: "space-between",
    },

    quantityButton: {
        width: 36,
        height: 36,
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
        fontSize: 18,
        fontWeight: "700",
        color: "#333",
        lineHeight: 20,
    },

    quantityText: {
        fontSize: 15,
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
});

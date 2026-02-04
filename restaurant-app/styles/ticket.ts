import { StyleSheet, Dimensions } from "react-native";
import { colors, spacing, spacingHelpers } from "./tokens";

const isShortScreen = Dimensions.get("window").height < 700;

export const ticket_style = StyleSheet.create({
    container: {
        flex: 1,
        flexDirection: "column",
        padding: 16,
    },
    headerContainer: {
        flexDirection: "column",
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: "#ccc",
    },
    headerText: {
        fontSize: 14,
        marginBottom: 4,
    },
    table: {
        marginTop: 8,
        marginBottom: 12,
    },
    ordersScroll: {
        flexGrow: 1,
        paddingVertical: 8,
    },
    tableHeader: {
        flexDirection: "row",
        backgroundColor: "#f0f0f0",
        paddingVertical: 6,
        borderTopLeftRadius: 8,
        borderTopRightRadius: 8,
    },
    headerCol: {
        fontSize: 12,
        fontWeight: "bold",
        paddingHorizontal: 5,
    },
    totalHeader: {
        flex: 1.5,
        textAlign: "right",
    },
    tableRow: {
        flexDirection: "row",
        paddingVertical: 8,
        borderBottomWidth: 1,
        borderBottomColor: "#eee",
    },
    totalRow: {
        borderTopWidth: 2,
        borderTopColor: "#333",
        marginTop: 10,
        paddingVertical: 8,
    },
    emptyCol: { flex: 1 },
    totalAmount: {
        flex: 1.5,
        fontSize: 16,
        fontWeight: "bold",
        color: "green",
        textAlign: "right",
        paddingRight: 5,
    },
    syncOverlay: {
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.15)",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 999,
    },
    syncBox: {
        backgroundColor: "#fff",
        padding: 20,
        borderRadius: 12,
        flexDirection: "row",
        alignItems: "center",
        gap: 12,

        shadowColor: "#000",
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
        elevation: 8,
    },
    syncText: {
        fontSize: 14,
        fontWeight: "600",
    },
    commentsBox: {
        paddingHorizontal: 16,
        paddingVertical: 12,
        backgroundColor: "#fff",
        borderTopWidth: 1,
        borderTopColor: "#ebebeb",
    },
    commentsLabel: {
        fontSize: 14,
        fontWeight: "600",
        color: "#555",
        marginBottom: 6,
    },
    commentsInput: {
        minHeight: 42,
        maxHeight: 120,
        backgroundColor: "#f6f6f6",
        borderRadius: 8,
        paddingHorizontal: 10,
        paddingVertical: 8,
        fontSize: 14,
        color: "#333",
        textAlignVertical: "top",

        borderWidth: 1,
        borderColor: "#d0d0d0",
    },
    clientContainer: {
        paddingVertical: 10,
        borderBottomWidth: 1,
        borderBottomColor: "#e0e0e0",
    },

    clientLabel: {
        fontSize: 14,
        fontWeight: "500",
    },

    clientInput: {
        height: 40,
        paddingHorizontal: 4,
        fontSize: 14,
        color: "#333",

        borderWidth: 1,
        borderColor: "#d0d0d0",
        borderRadius: 6,
        backgroundColor: "#fafafa",
    },
    moreAboveHint: {
        fontSize: 12,
        color: "#888",
        marginBottom: 4,
        textAlign: "center",
    },
    metaSection: {},
    totalBar: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderTopWidth: 1,
        borderTopColor: "#e5e5e5",
        backgroundColor: "#fff",
    },

    totalLabel: {
        fontSize: 16,
        fontWeight: "600",
        color: "#444",
    },

    totalValue: {
        fontSize: 20,
        fontWeight: "700",
        color: "green",
    },
});

export const ticket_buttons_style = StyleSheet.create({
    container: {
        flexDirection: "row",
        flexWrap: "wrap",
        justifyContent: "center",
        paddingHorizontal: 12,
    },
    footer: {
        borderTopWidth: 1,
        borderTopColor: "#e5e5e5",
        backgroundColor: "#fff",
    },
    baseButton: {
        flexGrow: 1,
        minWidth: 120,
        height: 44,
        maxHeight: 50,
        borderRadius: 10,
        paddingVertical: 8,
        marginVertical: 5,
        marginHorizontal: 5,
        alignItems: "center",
        justifyContent: "center",
        borderColor: "#ddd",
        borderWidth: 1,
        backgroundColor: "#fff",

        // ios
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.12,
        shadowRadius: 18,

        // android
        elevation: 6,
    },
    buttonPressed: {
        opacity: 0.8,
        transform: [{ scale: 0.98 }],
    },
    text: {
        fontSize: 16,
        fontWeight: "600",
        textAlign: "center",
        flexWrap: "wrap",
    },
});

export const ticket_row_style = StyleSheet.create({
    column: {
        paddingHorizontal: 5,
    },
    textProduct: {
        fontSize: 14,
        fontWeight: "bold",
        color: "#333",
    },
    textAddon: {
        fontSize: 12,
        fontWeight: "400",
        color: "#555",
        marginRight: 2,
        flexWrap: "wrap",
    },
    addonsRow: {
        flexDirection: "row",
        flexWrap: "wrap",
    },
    quantityText: {
        fontSize: 14,
        fontWeight: "700",
        color: "#333",
        textAlign: "center",
    },
    totalText: {
        fontSize: 14,
        fontWeight: "700",
        color: "green",
        textAlign: "right",
    },
    deleteButton: {
        width: 20,
        height: 20,
        borderRadius: 10,
        alignItems: "center",
        justifyContent: "center",
        marginRight: 6,
    },

    deleteButtonPressed: {
        backgroundColor: "rgba(0,0,0,0.06)",
    },

    deleteButtonDisabled: {
        opacity: 0.4,
    },

    deleteButtonText: {
        fontSize: 14,
        fontWeight: "600",
        color: "#888",
        lineHeight: 16,
    },
});

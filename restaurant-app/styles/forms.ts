import { StyleSheet } from "react-native";
import { colors, spacing, spacingHelpers, typography } from "./tokens";

export const forms_style = StyleSheet.create({
    title: {
        fontSize: typography.size.xll,
        fontWeight: typography.weight.bold,
    },
    input: {
        width: "100%",
        borderWidth: 1,
        borderColor: "#cccc",
        borderRadius: 8,
        padding: 12,
        marginBottom: 12,
    },
    passwordContainer: {
        flexDirection: "row",
        alignItems: "center",
        width: "100%",
        marginBottom: 12,
    },
    showButton: {
        marginLeft: 8,
        paddingVertical: 12,
        paddingHorizontal: 10,
        borderRadius: 8,
        backgroundColor: "#f0f0f0",
    },
    showButtonText: {
        color: "#555",
        fontWeight: "500",
    },
    error: {
        color: "red",
        marginBottom: 12,
        textAlign: "center",
    },
    backButton: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        backgroundColor: "#f0f0f0",
        maxWidth: "70%",
    },
    backButtonText: {
        fontSize: 15,
        fontWeight: "500",
        color: "#555",
        textAlign: "center",
    },
    pressedEffect: {
        opacity: 0.85,
        transform: [{ scale: 0.97 }],
    },
    deleteText: {
        color: "#c62828",
    },
});

export const menu_style = StyleSheet.create({
    addButton: {
        flex: 1,
        minHeight: 48,
        backgroundColor: "#4CAF50",
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
        marginLeft: 12,

        shadowColor: "#4CAF50",
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.18,
        shadowRadius: 5,
        elevation: 4,
    },

    addButtonText: {
        fontSize: 16,
        fontWeight: "700",
        color: "#ffffff",
    },

    secondaryButton: {
        flex: 1,
        minHeight: 48,
        backgroundColor: "#e0e0e0",
        borderRadius: 12,
        alignItems: "center",
        justifyContent: "center",
    },

    secondaryButtonText: {
        fontSize: 15,
        fontWeight: "600",
        color: "#333",
    },
    searchInput: {
        minHeight: 44,
        backgroundColor: "#f2f2f2",
        borderRadius: 10,
        paddingHorizontal: 14,
        fontSize: 16,
        color: "#333",
        marginTop: 8,
        width: "100%",
    },
    headerContainer: {
        paddingHorizontal: 16,
        paddingTop: 14,
        paddingBottom: 12,
        backgroundColor: "#ffffff",
        borderBottomWidth: 1,
        borderBottomColor: "#ebebeb",

        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.08,
        shadowRadius: 6,
        elevation: 3,
    },
    footerContainer: {
        flexDirection: "row",
        paddingHorizontal: 16,
        paddingVertical: 12,
        backgroundColor: "#ffffff",
        borderTopWidth: 1,
        borderTopColor: "#ebebeb",

        shadowColor: "#000",
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: 0.1,
        shadowRadius: 6,
        elevation: 8,
    },
});

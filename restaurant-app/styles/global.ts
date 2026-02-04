import { StyleSheet } from "react-native";
import { colors, spacing, spacingHelpers } from "./tokens";

export const global_container_style = StyleSheet.create({
    layout_container: {
        flex: 1,
        backgroundColor: colors.background,
    },
    main_container: {
        flex: 1,
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        paddingHorizontal: spacing.md,
        gap: spacingHelpers.loose,
    },
    scroll_container: {
        paddingHorizontal: spacing.md,
        paddingVertical: spacingHelpers.section,
        gap: spacingHelpers.loose,

        flexGrow: 1,
        alignItems: "center",
    },
    gridContainer: {
        paddingHorizontal: 16,
        paddingTop: 16,
        paddingBottom: 16,
    },
    columnWrapper: {
        justifyContent: "space-between",
        marginBottom: 16,
    },
    backButton: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 8,
        paddingHorizontal: 10,
        borderRadius: 8,
        alignSelf: "flex-start",
        marginBottom: 8,
        backgroundColor: "#f0f0f0",
        maxWidth: "70%",
    },
    backButtonText: {
        fontSize: 15,
        fontWeight: "500",
        color: "#555",
        textAlign: "center",
    },
});

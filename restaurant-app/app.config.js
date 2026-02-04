require("dotenv").config({ path: "./.env" });

module.exports = ({ config }) => {
    const API_URL =
        process.env.PROD_FLASK_API_URL ||
        process.env.EXPO_PUBLIC_API_URL ||
        "http://localhost:5000";

    return {
        name: "Bestiario Restaurante App",
        slug: "restaurant-app",
        version: "1.0.0",
        orientation: "portrait",
        icon: "./assets/images/icon.png",
        scheme: "restaurantapp",
        userInterfaceStyle: "automatic",
        newArchEnabled: true,
        splash: {
            image: "./assets/images/splash-icon.png",
            resizeMode: "contain",
            backgroundColor: "#ffffff",
        },
        ios: {
            supportsTablet: true,
        },
        android: {
            adaptiveIcon: {
                foregroundImage: "./assets/images/adaptive-icon.png",
                backgroundColor: "#ffffff",
            },
            edgeToEdgeEnabled: true,
            predictiveBackGestureEnabled: false,
            package: "com.shiraoriwakaba.restaurantapp",
        },
        web: {
            bundler: "metro",
            output: "static",
            favicon: "./assets/images/favicon.png",
        },
        plugins: [
            "expo-router",
            [
                "expo-build-properties",
                {
                    android: {
                        usesCleartextTraffic: true,
                    },
                },
            ],
        ],
        experiments: {
            typedRoutes: true,
        },
        extra: {
            router: {},
            eas: {
                projectId: "db200e42-d575-4455-86e3-291ade23927f",
            },
            flaskApiUrl: API_URL,
        },
    };
};

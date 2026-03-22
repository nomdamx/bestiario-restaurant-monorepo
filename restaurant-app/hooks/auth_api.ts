import * as SecureStore from "expo-secure-store";
import { Session, User, SessionValidationResult } from "types/auth";
import Constants from "expo-constants";

const API_URL = Constants.expoConfig?.extra?.flaskApiUrl + "auth/";
const APP_VERSION = Constants.expoConfig?.extra?.appVersion;

const TOKEN_KEY = "session_token";

async function safeFetch(url: string, options?: RequestInit) {
    const res = await fetch(url, options);
    const text = await res.text();

    let json: any = null;
    try {
        json = text ? JSON.parse(text) : null;
    } catch {
        throw new Error(`Invalid JSON response from ${url}: ${text}`);
    }

    if (!res.ok) {
        throw new Error(json?.error || JSON.stringify(json));
    }

    return json;
}

export async function storeToken(token: string) {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
}

export async function getStoredToken(): Promise<string | null> {
    return SecureStore.getItemAsync(TOKEN_KEY);
}

export async function deleteStoredToken() {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
}

export async function generateSessionToken(): Promise<string> {
    const json = await safeFetch(API_URL + "session/token", {
        headers: { "X-App-Version": APP_VERSION },
    });
    return json.token;
}

export async function createSession(token: string, id_user: number) {
    await safeFetch(API_URL + `session`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-App-Version": APP_VERSION,
        },
        body: JSON.stringify({ id_user: id_user, token: token }),
    });
}

export async function validateSessionToken(
    token: string,
): Promise<SessionValidationResult> {
    const json = await safeFetch(API_URL + "session/validation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-App-Version": APP_VERSION,
        },
        body: JSON.stringify({ token }),
    });
    if (!json.user) return { session: null, user: null };
    return {
        session: {
            id_user: json.user.id,
            expires_at: new Date(json.expires_at * 1000),
        },
        user: {
            id: json.user.id,
            username: json.user.username,
            auth_level: json.user.auth_level,
            display_name: json.user.display_name,
        },
    };
}

export async function invalidateSession(token: string) {
    const res = await fetch(API_URL + "session", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-App-Version": APP_VERSION,
        },
        body: JSON.stringify({ token }),
    });

    if (!res.ok) {
        throw new Error(`Error invalidando sesión: ${res.statusText}`);
    }
}

export async function registerUser(
    username: string,
    password: string,
): Promise<User | null> {
    const json = await safeFetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-App-Version": APP_VERSION,
        },
        body: JSON.stringify({ username, password, display_name: username }),
    });

    return {
        id: json.id,
        username: json.username,
        auth_level: json.auth_level,
        display_name: json.display_name,
    };
}

export async function validateUser(
    username: string,
    password: string,
): Promise<User | null> {
    const json = await safeFetch(API_URL + "user/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-App-Version": APP_VERSION,
        },
        body: JSON.stringify({ username, password }),
    });

    if (json.username === username) {
        return {
            id: json.id,
            username: json.username,
            auth_level: json.auth_level,
            display_name: json.display_name,
        };
    }

    return null;
}

export async function check_need_password(): Promise<boolean> {
    const need_password_request = await fetch(API_URL + "system/password", {
        method: "GET",
        headers: { "X-App-Version": APP_VERSION },
    }).then((data) => data.json());
    return validateBool(need_password_request.value);
}

export async function check_admin_see_config(): Promise<boolean> {
    const admin_see_password = await fetch(API_URL + "system/config", {
        method: "GET",
        headers: { "X-App-Version": APP_VERSION },
    }).then((data) => data.json());
    return validateBool(admin_see_password.value);
}

function validateBool(text: string): boolean {
    return text.toLowerCase().trim() === "true";
}

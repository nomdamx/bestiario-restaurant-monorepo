import * as SecureStore from "expo-secure-store";
import { Session, User, SessionValidationResult } from "types/auth";
import Constants from "expo-constants";

const API_URL = Constants.expoConfig?.extra?.flaskApiUrl + "auth/user/";
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
    const json = await safeFetch(API_URL + "session-token");
    return json.token;
}

export async function createSession(
    token: string,
    userId: number,
): Promise<Session> {
    const json = await safeFetch(API_URL + `create-session/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
    });

    return {
        id: json.session,
        userId,
        expiresAt: new Date(json.expires_at * 1000),
    };
}

export async function validateSessionToken(
    token: string,
): Promise<SessionValidationResult> {
    const json = await safeFetch(API_URL + "session-validation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
    });

    if (!json.session) return { session: null, user: null };
    return {
        session: {
            id: json.session.session,
            userId: json.session.id_user,
            expiresAt: new Date(json.session.expires_at * 1000),
        },
        user: {
            id: json.user.id,
            username: json.user.username,
            auth_level: json.user.auth_level,
            display_name: json.user.display_name,
        },
    };
}

export async function invalidateSession(sessionId: string) {
    const res = await fetch(API_URL + "session-invalidation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session: sessionId }),
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (json?.error) return null;

    return {
        id: json.response[0].id,
        username: json.response[0].username,
        auth_level: json.response[0].auth_level,
        display_name: json.response[0].display_name,
    };
}

export async function validateUser(
    username: string,
    password: string,
): Promise<User | null> {
    const json = await safeFetch(API_URL + "user-validation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (json.response?.[0]?.username === username) {
        return {
            id: json.response[0].id,
            username: json.response[0].username,
            auth_level: json.response[0].auth_level,
            display_name: json.response[0].display_name,
        };
    }

    return null;
}

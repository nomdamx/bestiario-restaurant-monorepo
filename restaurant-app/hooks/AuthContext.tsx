import { createContext, useContext, useEffect, useMemo, useState } from "react";
import {
    getStoredToken,
    storeToken,
    deleteStoredToken,
    generateSessionToken,
    createSession,
    validateSessionToken,
    invalidateSession,
    validateUser,
    registerUser,
} from "hooks/auth_api";
import { Session, User } from "types/auth";

interface AuthContextType {
    user: User | null;
    session: Session | null;
    loading: boolean;
    login: (userId: number) => Promise<void>;
    loginWithUser: (username: string, password: string) => Promise<boolean>;
    register: (username: string, password: string) => Promise<User | null>;
    logout: () => Promise<void>;
    authFetch: (url: string, options: RequestInit) => Promise<Response>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        bootstrap();
    }, []);

    async function bootstrap() {
        try {
            const token = await getStoredToken();
            if (!token) {
                setLoading(false);
                return;
            }

            const { session, user } = await validateSessionToken(token);

            if (!session || !user) {
                await deleteStoredToken();
                return;
            }
            setSession(session);
            setUser(user);
        } catch (error) {
            console.warn("Auth bootstrap failed:", error);
            await deleteStoredToken();
        } finally {
            setLoading(false);
        }
    }

    async function login(userId: number) {
        try {
            const token = await generateSessionToken();
            await createSession(token, userId);

            await storeToken(token);

            const validation = await validateSessionToken(token);
            if (!validation.session || !validation.user) {
                throw new Error("Invalid session after login");
            }

            setSession(validation.session);
            setUser(validation.user);
        } catch (error) {
            await deleteStoredToken();
            setSession(null);
            setUser(null);
            throw error;
        }
    }

    async function loginWithUser(username: string, password: string) {
        try {
            const user = await validateUser(username, password);
            if (!user) return false;

            await login(user.id);
            return true;
        } catch {
            return false;
        }
    }

    async function register(username: string, password: string) {
        try {
            const user = await registerUser(username, password);
            if (!user) return null;

            await login(user.id);
            return user;
        } catch {
            await deleteStoredToken();
            setSession(null);
            setUser(null);
            return null;
        }
    }

    async function logout() {
        if (loading) return;
        setLoading(true);
        try {
            if (session) {
                await invalidateSession(session.id);
            }
        } catch (error) {
            console.warn("Error invalidando la sesión:", error);
        } finally {
            await deleteStoredToken();
            setSession(null);
            setUser(null);
            setLoading(false);
        }
    }

    async function authFetch(url: string, options: RequestInit = {}) {
        const token = await getStoredToken();

        return fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                Authorization: `Bearer ${token}`,
                Accept: "application/vnd.restaurant-api.v1+json",
                "X-App-Version": "vapp-0.1.0",
            },
        });
    }

    const value = useMemo(
        () => ({
            user,
            session,
            loading,
            login,
            loginWithUser,
            register,
            logout,
            authFetch,
        }),
        [user, session, loading],
    );

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be inside AuthProvider");
    return ctx;
}

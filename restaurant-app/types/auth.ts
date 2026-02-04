export interface Session {
    id: string;
    userId: number;
    expiresAt: Date;
}

export interface User {
    id: number;
    username: string;
    auth_level: string;
    display_name: string;
}

export type SessionValidationResult =
    | { session: Session; user: User }
    | { session: null; user: null };

export interface CreateSessionPayload {
    token: string;
    userId: number;
}

export interface InvalidateSessionPayload {
    sessionId: string;
}

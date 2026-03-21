export interface Session {
    id_user: number;
    expires_at: Date;
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
    id_user: number;
}

export interface InvalidateSessionPayload {
    session_id: string;
}

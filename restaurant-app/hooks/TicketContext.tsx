import { createContext, useContext } from "react";
import { useStoreTicket } from "./useStoreTicket";

type TicketContextType = ReturnType<typeof useStoreTicket>;

const TicketContext = createContext<TicketContextType | null>(null);

export function TicketProvider({ children }: { children: React.ReactNode }) {
    const store = useStoreTicket();

    return (
        <TicketContext.Provider value={store}>
            {children}
        </TicketContext.Provider>
    );
}

export function useTicket() {
    const context = useContext(TicketContext);
    if (!context) {
        throw new Error("useTicket must be used inside TicketProvider");
    }
    return context;
}

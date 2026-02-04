import { NavButton } from "components/NavButton";
import { useTicket } from "hooks/TicketContext";
import { useEffect } from "react";
import { View } from "react-native";

import { global_container_style } from "styles/global";

export default function HomeScreen() {
    const { setTicket } = useTicket();

    useEffect(() => {
        setTicket(null);
    }, [setTicket]);

    return (
        <View style={global_container_style.main_container}>
            <NavButton text="Pedidos" path="./orders" />
            <NavButton text="Cobrar" path="/orders/active_tables" />
            <NavButton text="Para llevar" path="/orders/togo" />
            <NavButton text="Menu" path="/orders/menu" />
        </View>
    );
}

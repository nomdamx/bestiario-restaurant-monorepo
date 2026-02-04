import { useState, useEffect } from "react";
import { Text } from "react-native";

function formatElapsedTime(timestamp: string) {
    const now = new Date();
    const created = new Date(timestamp);

    const diffMs = now.getTime() - created.getTime();

    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

    const pad = (n: number) => String(n).padStart(2, "0");

    return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

interface TimerProps {
    timestamp: string;
}

export function TimerText({ timestamp }: TimerProps) {
    const [elapsed, setElapsed] = useState(() => formatElapsedTime(timestamp));

    useEffect(() => {
        const interval = setInterval(() => {
            setElapsed(formatElapsedTime(timestamp));
        }, 1000);

        return () => clearInterval(interval);
    }, [timestamp]);

    return <Text>{elapsed}</Text>;
}

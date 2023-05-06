import React from "react";
import io, { Socket } from "socket.io-client";

import { ClientEvents, ServerEvents } from "@puzzled/messages";

interface SocketContextData {
	socket: Socket<ServerEvents, ClientEvents>;
}

const SocketContext = React.createContext<SocketContextData | undefined>(undefined);

interface Props {
	children: React.ReactNode;
}

export const SocketProvider = (props: Props) => {
	const [socket, setSocket] = React.useState<Socket<ServerEvents, ClientEvents> | undefined>(undefined);

	React.useEffect(() => {
		const url = `ws://${window.location.hostname}:${window.location.port}`;
		const newSocket: Socket<ServerEvents, ClientEvents> = io(url, {
			transports: ["websocket"]
		});
		setSocket(newSocket);

		return () => {
			newSocket.disconnect();
		};
	}, []);

	if (socket === undefined) {
		return null; // TODO: show something here
	}

	return (
		<SocketContext.Provider value={{ socket }}>
			{props.children}
		</SocketContext.Provider>
	);
};

export const useSocket = () => {
	const socket = React.useContext(SocketContext);

	if (socket === undefined) {
		throw new Error("useSocket must be used within a SocketProvider");
	}

	return socket;
};

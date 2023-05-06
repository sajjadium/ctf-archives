import { List } from "immutable";
import React from "react";
import io, { Socket } from "socket.io-client";

import { ClientEvent, ServerEvent } from "@amongst/messages";

const MinPingChecks = 5;
const MaxPingChecks = 10;
const PingInterval = 2000;

interface SocketContextData {
	socket: Socket<ServerEvent, ClientEvent>;
	ping: number;
}

const SocketContext = React.createContext<SocketContextData | undefined>(undefined);

interface Props {
	gameId: string;
	name: string;
	host?: string;
	port: number;
	children: React.ReactNode;
}

export const SocketProvider = (props: Props) => {
	const [socket, setSocket] = React.useState<Socket<ServerEvent, ClientEvent> | undefined>(undefined);
	const [pingChecks, setPingChecks] = React.useState<List<number>>(List());

	React.useEffect(() => {
		const url = `ws://${props.host ?? window.location.hostname}:${props.port}`;
		const newSocket: Socket<ServerEvent, ClientEvent> = io(url, {
			transports: ["websocket"],
			query: {
				game: props.gameId,
				name: props.name
			}
		});
		setSocket(newSocket);

		return () => {
			newSocket.disconnect();
		};
	}, [props.gameId]);

	React.useEffect(() => {
		if (socket !== undefined) {
			const controller: AbortController = new AbortController();

			const doPingCheck = () => {
				const start = Date.now();
				socket.emit("ping", () => {
					if (!controller.signal.aborted) {
						setPingChecks(pingChecks.push(Date.now() - start).takeLast(MaxPingChecks));
					}
				});
			};

			if (pingChecks.size < MinPingChecks) {
				// Do an immediate ping check to populate the initial ping value
				doPingCheck();

				return () => {
					controller.abort();
				};
			} else {
				// Do a ping check in `PingInterval` milliseconds
				const timeout = setTimeout(doPingCheck, PingInterval);

				return () => {
					clearTimeout(timeout);
					controller.abort();
				};
			}
		}
	}, [socket, pingChecks]);

	if (socket === undefined || pingChecks.size < 5) {
		return null; // TODO: show something here
	}

	return (
		<SocketContext.Provider
			value={{
				socket,
				ping: pingChecks.reduce((sum, cur) => sum + cur, 0) / pingChecks.size
			}}
		>
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

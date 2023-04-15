import React from "react";

import { ServerEvents } from "@puzzled/messages";
import { GameState } from "@puzzled/types";

import { useSocket } from "./useSocket.js";

const GameStateContext = React.createContext<GameState | undefined>(undefined);

interface Props {
	children: React.ReactNode;
}

export const GameStateProvider = (props: Props) => {
	const [gameState, setGameState] = React.useState<GameState | undefined>(undefined);
	const { socket } = useSocket();

	React.useEffect(() => {
		const onState: ServerEvents["state"] = (gameStateJson) => setGameState(GameState.fromJson(gameStateJson));

		socket.on("state", onState);

		return () => {
			socket.off("state", onState);
		};
	}, [socket]);

	return (
		<GameStateContext.Provider value={gameState}>
			{props.children}
		</GameStateContext.Provider>
	);
};

export const useGameState = () => React.useContext(GameStateContext);

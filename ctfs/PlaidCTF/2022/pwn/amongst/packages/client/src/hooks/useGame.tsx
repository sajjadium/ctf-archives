import React from "react";

import { Game } from "@amongst/game-client";
import { GameSync, GameUpdateBundle } from "@amongst/messages";

import { useSocket } from "./useSocket";

const GameContext = React.createContext<Game | undefined>(undefined);

export const GameProvider = (props: { children: React.ReactNode }) => {
	const { socket } = useSocket();
	const [game, setGame] = React.useState<Game | undefined>(undefined);

	React.useEffect(() => {
		socket.emit("join");
	}, [socket]);

	React.useEffect(() => {
		const onGameSync = (sync: GameSync) => {
			if (game === undefined) {
				setGame(Game.fromSync(sync, socket));
			} else {
				// eslint-disable-next-line no-console
				console.warn("Required to resync");
				game.copyFrom(Game.fromSync(sync, socket));
			}
		};

		socket.on("sync", onGameSync);

		const onGameUpdate = (bundle: GameUpdateBundle) => {
			if (game === undefined) {
				return;
			}

			game.applyUpdates(bundle);
		};

		socket.on("update", onGameUpdate);

		return () => {
			socket.off("sync", onGameSync);
			socket.off("update", onGameUpdate);
		};
	}, [socket, game]);

	return (
		<GameContext.Provider value={game}>
			{props.children}
		</GameContext.Provider>
	);
};

export const useGame = () => React.useContext(GameContext);

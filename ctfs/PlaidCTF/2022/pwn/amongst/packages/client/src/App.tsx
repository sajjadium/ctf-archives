import React from "react";

import { GameView } from "./views/GameView";
import { LaunchView } from "./views/LaunchView";

export const App = () => {
	const [gameInfo, setGameInfo] =
		React.useState<{ id: string; host?: string; port: number; name: string } | undefined>();

	if (gameInfo === undefined) {
		return (
			<LaunchView
				onJoinGame={setGameInfo}
			/>
		);
	} else {
		return (
			<GameView
				gameId={gameInfo.id}
				host={gameInfo.host}
				port={gameInfo.port}
				name={gameInfo.name}
			/>
		);
	}
};

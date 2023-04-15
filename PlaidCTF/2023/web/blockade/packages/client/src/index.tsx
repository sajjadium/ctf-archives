import React from "react";
import { createRoot } from "react-dom/client";

import { App } from "./components/App/index.js";
import { BoardInfoProvider } from "./hooks/useBoardInfo.js";
import { GameStateProvider } from "./hooks/useGameState.js";
import { SocketProvider } from "./hooks/useSocket.js";

import "./index.scss";

const root = createRoot(document.getElementById("root")!);
root.render(
	<SocketProvider>
		<BoardInfoProvider>
			<GameStateProvider>
				<App />
			</GameStateProvider>
		</BoardInfoProvider>
	</SocketProvider>
);

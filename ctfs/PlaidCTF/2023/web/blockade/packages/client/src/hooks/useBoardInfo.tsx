import React from "react";

import { ServerEvents } from "@puzzled/messages";
import { BoardInfo } from "@puzzled/types";

import { useSocket } from "./useSocket.js";

const BoardInfoContext = React.createContext<BoardInfo | undefined>(undefined);

interface Props {
	children: React.ReactNode;
}

export const BoardInfoProvider = (props: Props) => {
	const [boardInfo, setBoardInfo] = React.useState<BoardInfo | undefined>(undefined);
	const { socket } = useSocket();

	React.useEffect(() => {
		const onBoard: ServerEvents["board"] = (boardInfoJson) => setBoardInfo(BoardInfo.fromJson(boardInfoJson));

		socket.on("board", onBoard);

		return () => {
			socket.off("board", onBoard);
		};
	}, [socket]);

	return (
		<BoardInfoContext.Provider value={boardInfo}>
			{props.children}
		</BoardInfoContext.Provider>
	);
};

export const useBoardInfo = () => React.useContext(BoardInfoContext);

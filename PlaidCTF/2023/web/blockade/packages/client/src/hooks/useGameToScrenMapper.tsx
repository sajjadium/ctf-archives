import React from "react";

import { Point as GamePoint } from "@puzzled/types";

import { ScreenPoint } from "@/types/ScreenPoint.js";

type GameToScreenMapper = (point: GamePoint) => ScreenPoint;

const GameToScreenMapperContext = React.createContext<GameToScreenMapper | undefined>(undefined);

export const GameToScreenMapperProvider = (props: { children: React.ReactNode; mapper: GameToScreenMapper }) => {
	return (
		<GameToScreenMapperContext.Provider value={props.mapper}>
			{props.children}
		</GameToScreenMapperContext.Provider>
	);
};

export const useGameToScreenMapper = () => {
	const mapper = React.useContext(GameToScreenMapperContext);

	if (mapper === undefined) {
		throw new Error("useGameToScreenMapper must be used within a GameToScreenMapperProvider");
	}

	return mapper;
};

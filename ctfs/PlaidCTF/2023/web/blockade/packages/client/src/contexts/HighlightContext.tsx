import React from "react";

export type HighlightTarget =
	| { kind: "ship"; id: number }
	| { kind: "faction"; id: number }
	;

interface ContextValue {
	highlight?: HighlightTarget;
	setHighlight: (target?: HighlightTarget) => void;
}

const HighlightContext = React.createContext({
	highlight: undefined,
	setHighlight: (target) => {},
} as ContextValue);

export const HighlightProvider = HighlightContext.Provider;
export const useHighlight = () => {
	const { highlight, setHighlight } = React.useContext(HighlightContext);
	return [highlight, setHighlight] as const;
};

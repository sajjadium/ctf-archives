import React from "react";

export const usePrevious = <S, T>(clock: S, value: T, initPrevious: T) => {
	const clockRef = React.useRef<S>(clock);
	const previousRef = React.useRef<T>(initPrevious);
	const currentRef = React.useRef<T>(value);

	if (clockRef.current !== clock) {
		previousRef.current = currentRef.current;
		currentRef.current = value;
		clockRef.current = clock;
	}

	return previousRef.current;
};

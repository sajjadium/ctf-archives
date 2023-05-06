import { Set } from "immutable";
import React from "react";

export const useKeyboard = () => {
	const [keys, setKeys] = React.useState(Set<string>());

	const onKeyDown = React.useCallback((event: KeyboardEvent) => {
		if (!event.repeat) {
			setKeys((current) => current.add(event.code));
		}
	}, []);

	const onKeyUp = React.useCallback((event: KeyboardEvent) => {
		if (!event.repeat) {
			setKeys((current) => current.remove(event.code));
		}
	}, []);

	React.useEffect(() => {
		window.addEventListener("keydown", onKeyDown);
		window.addEventListener("keyup", onKeyUp);

		return () => {
			window.removeEventListener("keydown", onKeyDown);
			window.removeEventListener("keyup", onKeyUp);
		};
	}, []);

	return keys;
};

export const useKeyboardTrigger = <S, >(clock: S) => {
	const [keys, setKeys] = React.useState(Set<string>());

	const onKeyDown = React.useCallback((event: KeyboardEvent) => {
		if (!event.repeat) {
			setKeys((current) => current.add(event.code));
		}
	}, []);

	React.useEffect(() => {
		window.addEventListener("keydown", onKeyDown);

		return () => {
			window.removeEventListener("keydown", onKeyDown);
		};
	}, []);

	React.useEffect(() => {
		setKeys(Set());
	}, [clock]);

	return keys;
};

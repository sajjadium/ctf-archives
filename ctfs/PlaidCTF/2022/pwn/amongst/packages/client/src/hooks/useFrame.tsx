import React from "react";

export const useFrame = (callback: (delta: number) => void) => {
	const lastFrameRef = React.useRef(Date.now());
	const callbackRef = React.useRef(callback);

	callbackRef.current = callback;

	React.useEffect(() => {
		let currentRequestId: number | undefined;

		const frame = () => {
			const delta = Date.now() - lastFrameRef.current;
			lastFrameRef.current = Date.now();
			callbackRef.current(delta);
			currentRequestId = requestAnimationFrame(frame);
		};

		currentRequestId = requestAnimationFrame(frame);

		return () => {
			if (currentRequestId !== undefined) {
				cancelAnimationFrame(currentRequestId);
			}
		};
	}, []);
};

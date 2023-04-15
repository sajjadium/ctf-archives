import React from "react";

import { useAnimationFrame } from "./useAnimationFrame.js";

export const useProgress = (speed: number) => {
	const { time, reset } = useAnimationFrame();
	const [lastTime, setLastTime] = React.useState(0);
	const [progress, setProgress] = React.useState(0);

	React.useEffect(() => {
		setProgress((p) => p + (time - lastTime) * speed);
		setLastTime(time);
	}, [time, speed, lastTime]);

	return {
		progress,
		reset: () => {
			reset();
			setLastTime(0);
			setProgress(0);
		}
	};
};

import React from "react";

export const useAnimationFrame = () => {
	const [baseTime, setBaseTime] = React.useState(Date.now());
	const [time, setTime] = React.useState(Date.now());

	React.useEffect(() => {
		let raf: number;

		const tick = () => {
			setTime(Date.now());
			raf = requestAnimationFrame(tick);
		};

		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	}, []);

	const reset = React.useCallback(() => {
		setBaseTime(Date.now());
		setTime(Date.now());
	}, []);

	return {
		time: time - baseTime,
		reset
	};
};

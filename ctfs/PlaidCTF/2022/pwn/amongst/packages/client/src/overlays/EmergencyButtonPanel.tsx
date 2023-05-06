import React from "react";

import { EmergencyButtonController, Game } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./EmergencyButtonPanel.module.scss";

interface Props {
	game: Game;
	controller: EmergencyButtonController;
}

export const EmergencyButtonPanel = (props: Props) => {
	const [frameCount, setFrameCount] = React.useState(0);
	const [closing, setClosing] = React.useState(false);

	useFrame(() => {
		setFrameCount((fc) => fc + 1);
	});

	const close = () => {
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	return (
		<div
			className={classes(
				styles.emergencyButtonPanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background}></div>
			<div className={styles.panel}>
				<button
					className={styles.close}
					onClick={() => {
						if (closing) {
							return;
						}

						close();
					}}
				/>
				<div
					className={styles.button}
					onClick={() => {
						props.controller.press();
					}}
				/>
			</div>
		</div>
	);
};

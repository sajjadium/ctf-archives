import React from "react";

import { Game, RecalibrateEngineController } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes, clsIf } from "../utils/css";

import styles from "./RecalibrateEnginePanel.module.scss";

interface Props {
	game: Game;
	controller: RecalibrateEngineController;
}

export const RecalibrateEnginePanel = (props: Props) => {
	const [frameCount, setFrameCount] = React.useState(0);
	const [autoCloseCancelled, setAutoCloseCancelled] = React.useState(false);
	const [closing, setClosing] = React.useState(false);

	useFrame(() => {
		setFrameCount((fc) => fc + 1);
	});

	const close = () => {
		setAutoCloseCancelled(true);
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	let keypadLocked = false;
	let keypadFlash: number | undefined;

	if (props.controller.flash !== undefined) {
		const tickDelta = props.game.self.tick - props.controller.flash.start;
		const index = Math.floor(tickDelta / 10);

		if (index < props.controller.flash.pattern.length) {
			keypadLocked = true;

			if (tickDelta % 10 > 5) {
				keypadFlash = props.controller.flash.pattern[index];
			}
		}
	}

	React.useEffect(() => {
		if (props.controller.state.complete && !autoCloseCancelled) {
			const timeout = setTimeout(close, 2000);
			return () => clearTimeout(timeout);
		}
	}, [props.controller.state.complete, autoCloseCancelled]);

	return (
		<div
			className={classes(
				styles.recalibrateEnginePanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background} />
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
				<div className={styles.display}>{props.controller.display}</div>
				<div className={styles.keypad}>
					{
						Array.from(new Array(9), (_, i) => (
							<button
								key={i}
								className={classes(
									styles.keypadButton,
									clsIf(keypadFlash === i + 1, styles.flash),
									clsIf(keypadLocked, styles.locked)
								)}
								disabled={keypadLocked}
								onClick={() => {
									if (closing) {
										return;
									}

									props.controller.send(i + 1);

									if (props.controller.state.complete) {
										setAutoCloseCancelled(true);
									}
								}}
							/>
						))
					}
				</div>
			</div>
		</div>
	);
};

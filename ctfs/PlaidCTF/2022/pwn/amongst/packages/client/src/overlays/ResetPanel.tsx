import React from "react";

import { Game, ResetController } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./ResetPanel.module.scss";

interface Props {
	game: Game;
	controller: ResetController;
}

export const ResetPanel = (props: Props) => {
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
				styles.resetPanel,
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
				<div className={styles.content}>
					<div className={styles.playerInfo}>
						{
							props.game.others.size < 2 ?
								"Waiting for more players..." :
							props.game.others.size < 6 ?
								<>
									{"There will be "}
									<span className={styles.shipmates}>{props.game.others.size} shipmates</span>
									{" and "}
									<span className={styles.hoaxers}>1 hoaxer</span>
									{"."}
								</> :
							<>
								{"There will be "}
								<span className={styles.shipmates}>{props.game.others.size - 1} shipmates</span>
								{" and "}
								<span className={styles.hoaxers}>2 hoaxers</span>
								{"."}
							</>
						}
					</div>
					{
						props.game.others.size >= 2
							? (
								<div
									className={styles.start}
									onClick={() => props.controller.start()}
								>
									Start
								</div>
							)
							: undefined
					}
				</div>
			</div>
		</div>
	);
};

import React from "react";

import { Game, VentController } from "@amongst/game-client";

import styles from "./VentOverlay.module.scss";

interface Props {
	game: Game;
	controller: VentController;
}

export const VentOverlay = (props: Props) => (
	<div className={styles.ventOverlay}>
		<button
			className={styles.close}
			onClick={() => props.controller.exit(props.game, props.game.self)}
		/>
		{
			props.controller.state.devices.map((device) => (
				<div
					className={styles.vent}
					onClick={() => props.controller.moveTo(props.game, props.game.self, device)}
				>
					<div className={styles.icon} />
					<div className={styles.name}>{device}</div>
				</div>
			))
		}
	</div>
);

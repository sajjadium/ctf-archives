import React from "react";

import { Game, SettingsController } from "@amongst/game-client";
import { Color } from "@amongst/game-common";

import { getSpotColors } from "../utils/color";

import styles from "./SettingsPanel.module.scss";

interface Props {
	game: Game;
	controller: SettingsController;
}

export const SettingsPanel = (props: Props) => (
	<div className={styles.settingsPanel}>
		<div className={styles.colors}>
			{
				Color.List.map((color) => (
					<div
						key={color}
						className={styles.color}
						style={{
							backgroundColor: "#" + getSpotColors(color).primary.toString(16).padStart(6, "0")
						}}
						onClick={() => props.controller.update(color, props.game.self.name)}
					/>
				))
			}
		</div>
		<button
			onClick={() => props.controller.exit(props.game, props.game.self)}
		>
			Close
		</button>
	</div>
);

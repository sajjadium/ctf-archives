import React from "react";

import { Game } from "@amongst/game-client";
import { MsPerTick, SystemKind } from "@amongst/game-common";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./TaskList.module.scss";

interface Props {
	game: Game;
}

export const TaskList = (props: Props) => {
	const [tick, setTick] = React.useState(Math.floor(props.game.self.tick));

	useFrame(() => {
		setTick(Math.floor(props.game.self.tick));
	});

	if (props.game.level.map.id !== "shelld") {
		return null;
	}

	return (
		<div className={styles.taskList}>
			{
				props.game.level.systems.valueSeq().map((system) => {
					switch (system.kind) {
						case SystemKind.ProvideCredentials: {
							return (
								<div
									key={system.id}
									className={classes(
										styles.task,
										system.complete ? styles.complete : styles.incomplete
									)}
								>
									Admin: Provide Credentials
								</div>
							);
						}

						case SystemKind.RecalibrateEngine: {
							return (
								<div
									key={system.id}
									className={classes(
										styles.task,
										system.complete ? styles.complete : styles.incomplete
									)}
								>
									Lower Engine: Recalibrate Engine
								</div>
							);
						}

						case SystemKind.PurchaseSnack: {
							return (
								<div
									key={system.id}
									className={classes(
										styles.task,
										system.complete ? styles.complete : styles.incomplete
									)}
								>
									Cafeteria: Purchase Snack
								</div>
							);
						}

						case SystemKind.ProcessSample: {
							const started = system.timerEndsAt !== undefined;
							const ticksRemaining = (
								system.timerEndsAt !== undefined
									? Math.max(system.timerEndsAt - tick, 0)
									: 0
							);
							const secondsRemaining = Math.ceil(ticksRemaining * MsPerTick / 1000);

							return (
								<div
									key={system.id}
									className={classes(
										styles.task,
										(
											system.taskComplete ? styles.complete :
											started ? styles.partial :
											styles.incomplete
										)
									)}
								>
									{"Medbay: Process Sample "}
									{
										system.taskComplete ? "(2/2)" :
										system.role === "begin" && !started ? "(0/2)" :
										system.role === "begin" && started ? (
											ticksRemaining > 0
												? `(1/2, ETA ${secondsRemaining}s)`
												: "(1/2, waiting on another shipmate)"
										) :
										system.role === "end" && !started ? "(0/2, waiting on another shipmate)" :
										system.role === "end" && started ? (
											ticksRemaining > 0
												? `(1/2, ETA ${secondsRemaining}s)`
												: "(1/2, ready)"
										) :
										"" // ???
									}
								</div>
							);
						}

						case SystemKind.FileTransfer: {
							return (
								<div
									key={system.id}
									className={classes(
										styles.task,
										(
											system.downloadComplete && system.uploadComplete ? styles.complete :
											system.downloadComplete ? styles.partial :
											styles.incomplete
										)
									)}
								>
									{
										system.downloadComplete && system.uploadComplete ? "Admin: Upload File (2/2)" :
										system.downloadComplete ? "Admin: Upload File (1/2)" :
										"Communications: Download File (0/2)"
									}
								</div>
							);
						}

						default: return undefined;
					}
				})
			}
		</div>
	);
};

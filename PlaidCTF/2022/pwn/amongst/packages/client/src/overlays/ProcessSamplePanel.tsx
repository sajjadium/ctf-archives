import React from "react";

import { Game, ProcessSampleController } from "@amongst/game-client";
import { MsPerTick } from "@amongst/game-common";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./ProcessSamplePanel.module.scss";

interface Props {
	game: Game;
	controller: ProcessSampleController;
}

export const ProcessSamplePanel = (props: Props) => {
	if (props.controller.state.role === "begin") {
		return <ProcessSampleBeginPanel {...props} />;
	} else {
		return <ProcessSampleEndPanel {...props} />;
	}
};

const ProcessSampleBeginPanel = (props: Props) => {
	const taskState = props.controller.state;
	const [currentTick, setCurrentTick] = React.useState(props.game.self.tick);
	const [loaded, setLoaded] = React.useState(taskState.timerEndsAt !== undefined);
	const [testTubePosition, setTestTubePosition] = React.useState([0, 0]);
	const [testTubeDragging, setTestTubeDragging] = React.useState(false);
	const [closing, setClosing] = React.useState(false);
	const [frameCount, setFrameCount] = React.useState(0);
	const [autoCloseCancelled, setAutoCloseCancelled] = React.useState(false);

	useFrame(() => {
		setFrameCount((fc) => fc + 1);
		setCurrentTick(props.game.self.tick);
	});

	const close = () => {
		setAutoCloseCancelled(true);
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	React.useEffect(() => {
		if (props.controller.state.taskComplete && !autoCloseCancelled) {
			const timeout = setTimeout(close, 2000);
			return () => clearTimeout(timeout);
		}
	}, [props.controller.state.taskComplete, autoCloseCancelled]);

	const testTubeInPosition = (
		250 <= testTubePosition[0]
		&& testTubePosition[0] <= 480
		&& 0 <= testTubePosition[1]
		&& testTubePosition[1] <= 200
	);

	React.useEffect(() => {
		if (testTubeDragging) {
			const onMouseMove = (event: MouseEvent) => {
				setTestTubePosition((pos) => [pos[0] + event.movementX, pos[1] + event.movementY]);
			};

			const onMouseUp = () => {
				setTestTubeDragging(false);
			};

			window.addEventListener("mousemove", onMouseMove);
			window.addEventListener("mouseup", onMouseUp);
			window.addEventListener("mouseleave", onMouseUp);

			return () => {
				window.removeEventListener("mousemove", onMouseMove);
				window.removeEventListener("mouseup", onMouseUp);
				window.removeEventListener("mouseleave", onMouseUp);
			};
		} else {
			if (testTubeInPosition) {
				setLoaded(true);
				props.controller.begin(props.game, props.game.self);
			}
		}
	}, [testTubeDragging]);

	return (
		<div
			className={classes(
				styles.processSamplePanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background} />
			<div
				className={classes(
					styles.panel,
					!loaded ? styles.open : styles.closed,
					!loaded && testTubeInPosition ? styles.testTubeReady : undefined,
					testTubeDragging ? styles.dragActive : undefined
				)}
				onMouseDown={() => {
					if (taskState.taskComplete) {
						setAutoCloseCancelled(true);
					}
				}}
			>
				<button
					className={styles.close}
					onClick={() => {
						if (closing) {
							return;
						}

						close();
					}}
				/>
				<div className={styles.message}>
					<div>
						{
							!loaded
								? "Insert sample" :
							taskState.timerEndsAt === undefined
								? "Beginning cycle..." :
							taskState.timerEndsAt < currentTick
								? "Processing complete" :
							(
								"Processing (ETA: "
								+ Math.ceil((taskState.timerEndsAt - currentTick) * MsPerTick / 1000).toString()
								+ "s)"
							)
						}
					</div>
					<div>
						{
							loaded && props.controller.display !== undefined
								? `Sample ID: ${props.controller.display}`
								: ""
						}
					</div>
				</div>
				{
					!loaded
						? (
							<div
								className={classes(
									styles.testTube,
									testTubeDragging ? styles.dragging : undefined,
									testTubeInPosition ? styles.inPosition : undefined
								)}
								style={{
									left: testTubePosition[0],
									top: testTubePosition[1],
								}}
								onMouseDown={(e) => {
									setTestTubeDragging(true);
								}}
							/>
						)
						: undefined
				}
			</div>
		</div>
	);
};

const ProcessSampleEndPanel = (props: Props) => {
	const taskState = props.controller.state;
	const [currentTick, setCurrentTick] = React.useState(props.game.self.tick);
	const [closing, setClosing] = React.useState(false);
	const [frameCount, setFrameCount] = React.useState(0);
	const [autoCloseCancelled, setAutoCloseCancelled] = React.useState(false);

	useFrame(() => {
		setFrameCount((fc) => fc + 1);
		setCurrentTick(props.game.self.tick);
	});

	const close = () => {
		setAutoCloseCancelled(true);
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	React.useEffect(() => {
		if (props.controller.state.taskComplete && !autoCloseCancelled) {
			const timeout = setTimeout(close, 2000);
			return () => clearTimeout(timeout);
		}
	}, [props.controller.state.taskComplete, autoCloseCancelled]);

	React.useEffect(() => {
		if (taskState.timerEndsAt !== undefined && taskState.timerEndsAt < currentTick) {
			props.controller.end(props.game, props.game.self);
		}
	}, [taskState.timerEndsAt, currentTick]);

	return (
		<div
			className={classes(
				styles.processSamplePanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background} />
			<div
				className={classes(
					styles.panel,
					styles.closed
				)}
				onMouseDown={() => {
					if (taskState.taskComplete) {
						setAutoCloseCancelled(true);
					}
				}}
			>
				<button
					className={styles.close}
					onClick={() => {
						if (closing) {
							return;
						}

						close();
					}}
				/>
				<div className={styles.message}>
					<div>
						{
							taskState.timerEndsAt === undefined
								? "Waiting for sample" :
							taskState.timerEndsAt < currentTick
								? "Processing complete" :
							(
								"Processing (ETA: "
								+ Math.ceil((taskState.timerEndsAt - currentTick) * MsPerTick / 1000).toString()
								+ "s)"
							)
						}
					</div>
					<div>
						{
							props.controller.display !== undefined ? `Result Code: ${props.controller.display}` : ""
						}
					</div>
				</div>
			</div>
		</div>
	);
};

import React from "react";

import { FileTransferController, Game } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./FileTransferPanel.module.scss";

interface Props {
	game: Game;
	controller: FileTransferController;
}

export const FileTransferPanel = (props: Props) => {
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

	const isUploading = props.controller.state.downloadComplete;
	const fromText = isUploading ? "My Tablet" : "Onsite Storage";
	const toText = isUploading ? "Remote Server" : "My Tablet";
	const progress = (
		isUploading
			? props.controller.uploadPosition / props.controller.uploadTotal * 100
			: props.controller.downloadPosition / props.controller.downloadTotal * 100
	);

	return (
		<div
			className={classes(
				styles.fileTransferPanel,
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
				<div className={styles.transferDetails}>
					<div className={styles.transferFrom}>
						<div className={styles.folder} />
						<svg className={styles.name}>
							<text x="50%" y={16}>{fromText}</text>
						</svg>
					</div>
					<div className={styles.transferTo}>
						<div className={styles.folder} />
						<svg className={styles.name}>
							<text x="50%" y={16}>{toText}</text>
						</svg>
					</div>
					<div className={styles.progressContainer}>
						<div className={styles.progressBar}>
							<div
								className={styles.progressCompleted}
								style={{ width: `${progress}%` }}
							/>
						</div>
						<svg className={styles.progressText}>
							<text x="50%" y={16}>{progress.toFixed(0)}%</text>
						</svg>
					</div>
				</div>
			</div>
		</div>
	);
};

import React from "react";

import { Game, HoldController } from "@amongst/game-client";
import { HoldPurpose } from "@amongst/game-common";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./HoldOverlay.module.scss";

interface Props {
	game: Game;
	controller: HoldController;
}

export const HoldOverlay = (props: Props) => {
	const [tick, setTick] = React.useState(Math.floor(props.game.self.tick));

	useFrame(() => {
		setTick(Math.floor(props.game.self.tick));
	});

	const remainingTicks = props.controller.state.until - tick;
	const fadeOut = remainingTicks < 10;

	let extraClassName: string;
	let content: React.ReactNode;

	switch (props.controller.purpose.kind) {
		case HoldPurpose.Kind.GameStart: {
			extraClassName = styles.gameStart;
			content = (
				<div className={styles.content}>
					<div className={styles.roleLine}>
						{"You are a "}
						<span
							className={classes(
								styles.role,
								props.game.self.hoaxer ? styles.hoaxer : styles.shipmate
							)}
						>
							{props.game.self.hoaxer ? "Hoaxer" : "Shipmate"}
						</span>
					</div>
					<div className={styles.amongstLine}>
						{
							props.controller.purpose.hoaxers === 1
								? "There is 1 hoaxer amongst ourselves"
								: `There are ${props.controller.purpose.hoaxers} hoaxers amongst ourselves`
						}
					</div>
				</div>
			);

			break;
		}

		case HoldPurpose.Kind.VoteComplete: {
			extraClassName = styles.voteComplete;

			switch (props.controller.purpose.outcome.kind) {
				case "tie": {
					content = (
						<div className={styles.content}>
							Nobody was ejected.  (Tied)
						</div>
					);
					break;
				}

				case "skipped": {
					content = (
						<div className={styles.voteComplete}>
							Nobody was ejected.  (Skipped)
						</div>
					);
					break;
				}

				case "ejected": {
					const playerId = props.controller.purpose.outcome.player;
					const player = props.game.self.id === playerId ? props.game.self : props.game.others.get(playerId);

					if (player !== undefined) {
						content = (
							<div className={styles.voteComplete}>
								{player.name} was {player.hoaxer ? "" : "not"} a hoaxer.
							</div>
						);
					}
					break;
				}
			}

			break;
		}

		case HoldPurpose.Kind.MeetingStart: {
			extraClassName = styles.meetingStart;
			content = <></>;
			break;
		}

		case HoldPurpose.Kind.GameEnd: {
			extraClassName = styles.gameEnd;
			if (props.controller.purpose.shipmatesWin) {
				content = (
					<div className={classes(styles.content, styles.shipmatesWin)}>
						Shipmates win!
					</div>
				);
			} else {
				content = (
					<div className={classes(styles.content, styles.hoaxersWin)}>
						Hoaxers win!
					</div>
				);
			}
			break;
		}
	}

	return (
		<div
			className={classes(
				styles.holdOverlay,
				extraClassName,
				fadeOut ? styles.fadeOut : undefined
			)}
		>
			{content}
		</div>
	);
};

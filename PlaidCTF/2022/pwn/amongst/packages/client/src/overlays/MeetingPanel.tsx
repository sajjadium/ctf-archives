import React from "react";

import { Game, MeetingController, Player } from "@amongst/game-client";

import { useColorFilter } from "../hooks/useColorFilter";
import { classes } from "../utils/css";

import styles from "./MeetingPanel.module.scss";

interface Props {
	game: Game;
	controller: MeetingController;
}

export const MeetingPanel = (props: Props) => (
	<div className={styles.meetingPanel}>
		{/* <div>
			<div>{props.game.self.color}</div>
			<div>{props.game.self.name}</div>
			<button
				disabled={props.controller.selfVoted || props.game.self.dead}
				onClick={() => props.controller.vote(props.game.self.id)}
			>
				Vote
			</button>
		</div> */}
		<div className={styles.players}>
			<PlayerDisplay player={props.game.self} game={props.game} controller={props.controller} />
			{
				[...props.game.others.values()].map((player) => (
					<PlayerDisplay key={player.id} player={player} game={props.game} controller={props.controller} />
				))
			}
		</div>
		<button
			className={classes(
				styles.skipButton,
				(
					props.controller.selfVoted || props.game.self.dead || props.game.self.dead
						? styles.hidden
						: undefined
				)
			)}
			onClick={() => props.controller.vote(undefined)}
		>
			Skip
		</button>
	</div>
);

const PlayerDisplay = (props: { controller: MeetingController; game: Game; player: Player }) => {
	const colorFilter = useColorFilter(props.player.color);

	return (
		<div className={styles.player} key={props.player.id}>
			<div
				className={styles.icon}
				style={{
					filter: colorFilter
				}}
			/>
			<div className={styles.name}>{props.player.name}</div>
			<button
				className={classes(
					styles.voteButton,
					(
						props.controller.selfVoted || props.game.self.dead || props.player.dead
							? styles.hidden
							: undefined
					)
				)}
				onClick={() => props.controller.vote(props.player.id)}
			>
				Vote
			</button>
		</div>
	);
};

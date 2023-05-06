import { Map } from "immutable";
import React from "react";

import { ServerEvents } from "@puzzled/messages";
import { ShipRoundMoves } from "@puzzled/types";
import { Move } from "@puzzled/types";

import { HighlightProvider, HighlightTarget } from "@/contexts/HighlightContext.js";
import { useGameState } from "@/hooks/useGameState.js";
import { useSocket } from "@/hooks/useSocket.js";
import { classes } from "@/utils/css.js";

import { Button } from "../Button/Button.js";
import { GameDisplay } from "../GameDisplay/GameDisplay.js";
import { Instructions } from "../Instructions/Instructions.js";
import { OutlineText } from "../OutlineText/index.js";
import { ShipControls } from "../ShipControls/index.js";

import styles from "./App.module.scss";

export const App = () => {
	const { socket } = useSocket();
	const state = useGameState();
	const [moves, setMoves] = React.useState<Map<number, ShipRoundMoves>>(Map());
	const [flag, setFlag] = React.useState<string | undefined>(undefined);
	const [showInstructions, setShowInstructions] = React.useState(localStorage.getItem("hideInstructions") === null);
	const [speed, setSpeed] = React.useState(1);
	const [highlightTarget, setHighlightTarget] = React.useState<HighlightTarget | undefined>(undefined);

	React.useEffect(() => {
		const onMovesUpdated: ServerEvents["movesUpdated"] = (args) => {
			setMoves((m) => m.set(args.id, args.moves));
		};

		const onState: ServerEvents["state"] = () => {
			setMoves(Map());
		};

		const onFlag: ServerEvents["flag"] = (flag) => {
			setFlag(flag);
		};

		socket.on("movesUpdated", onMovesUpdated);
		socket.on("state", onState);
		socket.on("flag", onFlag);

		return () => {
			socket.off("movesUpdated", onMovesUpdated);
			socket.off("state", onState);
			socket.off("flag", onFlag);
		};
	}, [socket]);

	let scoreboard: React.ReactNode | undefined;

	if (state !== undefined) {
		const maxScore = Math.max(1, ...state.factions.map((faction) => faction.score));
		scoreboard = (
			<div className={styles.scoreboard}>
				<div className={styles.round}>
					{
						state === undefined ? "Loading..." :
						state.round < 75 ? `Round ${state.round + 1}` :
						"Game over"
					}
				</div>
				<div className={styles.scores}>
					{
						state?.factions.map((faction) => (
							<div
								key={faction.id}
								className={classes(
									styles.faction,
									styles[`faction${faction.id}`],
								)}
							>
								<OutlineText
									className={styles.name}
									onMouseEnter={() => setHighlightTarget({ kind: "faction", id: faction.id })}
									onMouseLeave={() => setHighlightTarget(undefined)}
								>
									{faction.name}
								</OutlineText>
								<div
									className={styles.scoreBar}
									style={{ width: `${(faction.score / maxScore) * 100}%` }}
								/>
								<OutlineText className={styles.score}>
									{faction.score}
								</OutlineText>
							</div>
						))
					}
				</div>
			</div>
		);
	}

	let message: React.ReactNode | undefined;

	if (flag !== undefined) {
		message = (
			<div className={classes(styles.message, styles.flag)}>
				Victory is ours!  {flag}
			</div>
		);
	} else if (state !== undefined && state.round >= 75 && state.factions[1].score >= state.factions[0].score) {
		message = (
			<div className={classes(styles.message, styles.gameOver)}>
				Avast, ye booched it!  Abandon ship!
			</div>
		);
	}

	return (
		<HighlightProvider value={{ highlight: highlightTarget, setHighlight: setHighlightTarget }}>
			<div className={styles.app}>
				{
					showInstructions
						? (
							<Instructions
								onClose={() => {
									localStorage.setItem("hideInstructions", "true");
									setShowInstructions(false);
								}}
							/>
						)
						: undefined
				}
				<GameDisplay className={styles.board} speed={speed} />
				{message}
				<div className={styles.sidebar}>
					{scoreboard}
					<div className={styles.speed}>
						<div className={styles.label}>
							Game Speed
						</div>
						<input
							className={styles.speedSlider}
							type="range"
							min="-1"
							max="3"
							value={Math.log2(speed)}
							onChange={(e) => setSpeed(2 ** parseFloat(e.target.value))}
						/>
						<div className={styles.value}>
							{speed}x
						</div>
					</div>
					<div className={styles.first}>
						{
							state !== undefined
								? (
									<>
										<OutlineText
											className={
												styles[`faction${((state?.round + 1) % state.factions.length + 1)}`]
											}
										>
											{state.factions[(state.round + 1) % state.factions.length].name}
										</OutlineText>
										{" will move first"}
									</>
								)
								: undefined
						}
					</div>
					<div className={styles.endTurn}>
						<Button
							className={styles.endTurnButton}
							onClick={() => {
								socket.emit("advanceRound", { round: (state?.round ?? 0) + 1 });
							}}
						>
							End turn
						</Button>
					</div>
					<div className={styles.ships}>
						{
							state?.ships
								.filter((ship) => ship.faction === 1)
								.map((ship) => (
									<ShipControls
										key={ship.id}
										ship={{
											...ship,
											forwardTokens: ship.forwardTokens ?? 0,
											leftTokens: ship.leftTokens ?? 0,
											rightTokens: ship.rightTokens ?? 0,
											loadedCannons: ship.loadedCannons ?? 0,
											cannonballs: ship.cannonballs ?? 0,
											damage: ship.damage ?? 0,
										}}
										moves={
											moves.get(ship.id)
											?? [Move.empty(), Move.empty(), Move.empty(), Move.empty()]
										}
										onMovesChange={(newMoves) => {
											setMoves(moves.set(ship.id, newMoves));
											socket.emit("setMoves", { id: ship.id, moves: newMoves });
										}}
									/>
								))
						}
					</div>
				</div>
			</div>
		</HighlightProvider>
	);
};

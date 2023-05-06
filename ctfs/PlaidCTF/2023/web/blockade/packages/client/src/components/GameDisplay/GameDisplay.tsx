import { List, Map } from "immutable";
import React from "react";

import { ServerEvents } from "@puzzled/messages";
import { GameState, Heading,Point as GamePoint, RoundOutcome, ShipType } from "@puzzled/types";

import { useBoardInfo } from "@/hooks/useBoardInfo.js";
import { useGameState } from "@/hooks/useGameState.js";
import { useProgress } from "@/hooks/useProgress.js";
import { useSocket } from "@/hooks/useSocket.js";
import { BuoyFrames, BuoySpritesheet } from "@/spritesheets/Buoy.js";
import { GustFrames,GustSpritesheet } from "@/spritesheets/Gust.js";
import { RockFrame,RockSpritesheet } from "@/spritesheets/Rock.js";
import { WhirlpoolFrames, WhirlpoolSpritesheet } from "@/spritesheets/Whirlpool.js";

import { Board } from "../Board/index.js";
import { GameObject } from "../GameObject/GameObject.js";
import { Brig, Frigate,Galleon,Sloop } from "../Ship/index.js";
import { ShipController } from "../ShipController/ShipController.js";
import { Sprite } from "../Sprite/Sprite.js";

interface Props {
	className?: string;
	speed: number;
}

interface PendingUpdate {
	state: GameState;
	outcome: RoundOutcome;
}

interface ReducerValue {
	active?: {
		update: PendingUpdate;
		turn: number;
		phase: number;
	};
	pending: List<PendingUpdate>;
}

type Action =
	| { kind: "append", update: PendingUpdate }
	| { kind: "advance" }
	;

const BasePhaseDuration = 500;

export const GameDisplay = (props: Props) => {
	const [{ active: activeUpdate }, dispatch] = (
		React.useReducer<React.Reducer<ReducerValue, Action>>((current, action) => {
			switch (action.kind) {
				case "append": {
					if (current.active === undefined) {
						return {
							active: {
								update: action.update,
								turn: 0,
								phase: 0,
							},
							pending: List(),
						};
					} else {
						return {
							active: current.active,
							pending: current.pending.push(action.update),
						};
					}
				}

				case "advance": {
					if (current.active === undefined) {
						return current;
					}

					if (current.active.phase === 2) {
						if (current.active.turn === current.active.update.outcome.size - 1) {
							if (current.pending.size === 0) {
								return {
									pending: List(),
								};
							} else {
								return {
									active: {
										update: current.pending.first()!,
										turn: 0,
										phase: 0,
									},
									pending: current.pending.rest(),
								};
							}
						} else {
							return {
								active: {
									...current.active,
									turn: current.active.turn + 1,
									phase: 0,
								},
								pending: current.pending,
							};
						}
					} else {
						return {
							active: {
								...current.active,
								phase: current.active.phase + 1,
							},
							pending: current.pending,
						};
					}
				}
			}
		}, {
			pending: List<PendingUpdate>(),
		})
	);

	const boardInfo = useBoardInfo();
	const state = useGameState();
	const { socket } = useSocket();
	const { progress, reset: resetProgress } = useProgress(props.speed / BasePhaseDuration);

	React.useEffect(() => {
		if (activeUpdate !== undefined) {
			resetProgress();
		}
	}, [activeUpdate !== undefined]);

	React.useEffect(() => {
		if (
			activeUpdate !== undefined
			&& ((activeUpdate.phase !== 2 && progress >= 1) || (activeUpdate.phase === 2 && progress >= 2))
		) {
			dispatch({ kind: "advance" });
			resetProgress();
		}
	}, [activeUpdate !== undefined, progress]);

	React.useEffect(() => {
		const onRound: ServerEvents["round"] = (outcome) => {
			dispatch({
				kind: "append",
				update: {
					outcome: RoundOutcome.fromJson(outcome),
					state: state!,
				},
			});

			if (activeUpdate === undefined) {
				resetProgress();
			}
		};

		socket.on("round", onRound);

		return () => {
			socket.off("round", onRound);
		};
	}, [socket, state, activeUpdate === undefined]);

	const baseState = React.useMemo(() => {
		return activeUpdate?.update.state ?? state;
	}, [activeUpdate, state]);

	const shipPositionInfo = React.useMemo(() => {
		let ships = Map<number, {
			sunk: boolean;
			at: {
				location: GamePoint;
				heading: Heading;
			};
			move?: {
				to: {
					location: GamePoint;
					heading: Heading;
				};
				intent: {
					location: GamePoint;
					heading: Heading;
				};
			};
			fire?: {
				left?: {
					hit: boolean;
					to: GamePoint;
				};
				right?: {
					hit: boolean;
					to: GamePoint;
				};
			};
		}>();

		if (baseState === undefined) {
			return ships;
		}

		for (const ship of baseState.ships) {
			ships = ships.set(ship.id, {
				sunk: ship.sunk,
				at: {
					location: ship.location,
					heading: ship.heading,
				},
			});
		}

		if (activeUpdate === undefined) {
			return ships;
		}

		for (let i = 0; i < activeUpdate.turn; i++) {
			const turnOutcome = activeUpdate.update.outcome.get(i)!;

			for (const [shipId, shipMove] of turnOutcome.shipMoves) {
				const ship = ships.get(shipId)!;
				ship.at.location = shipMove.uncontrolledMove.result.location;
				ship.at.heading = shipMove.uncontrolledMove.result.heading;
			}

			for (const sunkId of turnOutcome.sunk) {
				const ship = ships.get(sunkId)!;
				ship.sunk = true;
			}
		}

		const turnOutcome = activeUpdate.update.outcome.get(activeUpdate.turn)!;

		switch (activeUpdate.phase) {
			case 0: {
				for (const [shipId, shipMove] of turnOutcome.shipMoves) {
					const ship = ships.get(shipId)!;
					ship.move = {
						to: {
							location: shipMove.controlledMove.result.location,
							heading: shipMove.controlledMove.result.heading,
						},
						intent: {
							location: shipMove.controlledMove.intent.location,
							heading: shipMove.controlledMove.intent.heading,
						},
					};
				}
				break;
			}

			case 1: {
				for (const [shipId, shipMove] of turnOutcome.shipMoves) {
					const ship = ships.get(shipId)!;
					ship.at = shipMove.controlledMove.result;
					ship.move = {
						to: {
							location: shipMove.uncontrolledMove.result.location,
							heading: shipMove.uncontrolledMove.result.heading,
						},
						intent: {
							location: shipMove.uncontrolledMove.intent.location,
							heading: shipMove.uncontrolledMove.intent.heading,
						},
					};
				}
				break;
			}

			case 2: {
				for (const [shipId, shipMove] of turnOutcome.shipMoves) {
					const ship = ships.get(shipId)!;
					ship.at = shipMove.uncontrolledMove.result;
					ship.fire = {
						left: (
							shipMove.fire.left === undefined ?
								undefined :
							shipMove.fire.left.kind === "hit" ?
								{ to: shipMove.fire.left.location, hit: true } :
							shipMove.fire.left.kind === "miss" ?
								{
									to: (
										ship.at.location
											.add(Heading.toPoint(Heading.leftOf(ship.at.heading)).scale(3))
									),
									hit: false
								} :
							undefined // ???
						),
						right: (
							shipMove.fire.right === undefined ?
								undefined :
							shipMove.fire.right.kind === "hit" ?
								{ to: shipMove.fire.right.location, hit: true } :
							shipMove.fire.right.kind === "miss" ?
								{
									to: (
										ship.at.location
											.add(Heading.toPoint(Heading.rightOf(ship.at.heading)).scale(3))
									),
									hit: false
								} :
							undefined // ???
						),
					};
				}
				break;
			}
		}

		return ships;
	}, [activeUpdate, baseState]);

	return (
		<Board className={props.className} size={new GamePoint(20, 32)}>
			{
				baseState?.ships.map((ship) => {
					const positionInfo = shipPositionInfo.get(ship.id)!;

					if (positionInfo.sunk) {
						return null;
					}

					return (
						<ShipController
							key={ship.id}
							ship={
								ship.type === ShipType.Sloop ? Sloop :
								ship.type === ShipType.Brig ? Brig :
								ship.type === ShipType.Galleon ? Galleon :
								ship.type === ShipType.Frigate ? Frigate :
								Sloop // ???
							}
							at={positionInfo.at}
							move={positionInfo.move}
							fire={positionInfo.fire}
							progress={progress}
							info={{
								id: ship.id,
								name: ship.name,
								faction: ship.faction,
								sunk: ship.sunk,
							}}
						/>
					);
				})
			}
			{
				boardInfo?.rocks.map((rock, i) => (
					<GameObject key={`rock-${i}`} location={rock.location}>
						<Sprite
							spritesheet={RockSpritesheet}
							frame={RockFrame}
						/>
					</GameObject>
				))
			}
			{
				boardInfo?.gusts.map((gust, i) => (
					<GameObject key={`gust-${i}`} location={gust.location} layer={-1}>
						<Sprite
							spritesheet={GustSpritesheet}
							frame={GustFrames[gust.heading]}
						/>
					</GameObject>
				))
			}
			{
				boardInfo?.whirlpools.map((whirlpool, i) => (
					<GameObject key={`whirlpool-${i}`} location={whirlpool.location} layer={-1}>
						<Sprite
							spritesheet={WhirlpoolSpritesheet}
							frame={
								whirlpool.clockwise
									? WhirlpoolFrames.clockwise
									: WhirlpoolFrames.counterclockwise
							}
						/>
					</GameObject>
				))
			}
			{
				boardInfo?.buoys.map((buoy, i) => (
					<GameObject key={`buoy-${i}`} location={buoy.location}>
						<Sprite
							spritesheet={BuoySpritesheet}
							frame={BuoyFrames[buoy.value as 1 | 2 | 3]}
						/>
					</GameObject>
				))
			}
		</Board>
	);
};

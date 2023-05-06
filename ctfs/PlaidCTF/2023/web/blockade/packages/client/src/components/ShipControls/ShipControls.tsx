import React from "react";

import { Heading, MovementToken, ShipType } from "@puzzled/types";
import { Move } from "@puzzled/types";

import { useHighlight } from "@/contexts/HighlightContext.js";
import { BrigFrames, BrigHaloSpritesheet, BrigSpritesheet } from "@/spritesheets/Brig.js";
import { FrigateFrames, FrigateHaloSpritesheet, FrigateSpritesheet } from "@/spritesheets/Frigate.js";
import { GalleonFrames, GalleonHaloSpritesheet, GalleonSpritesheet } from "@/spritesheets/Galleon.js";
import { SloopFrames, SloopHaloSpritesheet, SloopSpritesheet } from "@/spritesheets/Sloop.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import { OutlineText } from "../OutlineText/OutlineText.js";
import { Sprite } from "../Sprite/index.js";
import { DraggableFireToken } from "./DraggableFireToken.js";
import { DraggableToken } from "./DraggableToken.js";

import styles from "./ShipControls.module.scss";

interface ShipInfo {
	id: number;
	name: string;
	type: ShipType;
	forwardTokens: number;
	leftTokens: number;
	rightTokens: number;
	loadedCannons: number;
	cannonballs: number;
	damage: number;
	sunk: boolean;
}

interface Props {
	className?: string;
	ship: ShipInfo;
	moves: [Move, Move, Move, Move];
	onMovesChange: (moves: [Move, Move, Move, Move]) => void;
}

let instanceIdCounter = 0;

export const ShipControls = (props: Props) => {
	const [highlightTarget, setHighlightTarget] = useHighlight();

	const instanceId = React.useState(() => (instanceIdCounter++).toString())[0];

	const remainingForwardTokens = (
		props.ship.forwardTokens
		- props.moves.reduce((total, move) => total + (move.token === MovementToken.Forward ? 1 : 0), 0)
	);

	const remainingLeftTokens = (
		props.ship.leftTokens
		- props.moves.reduce((total, move) => total + (move.token === MovementToken.Left ? 1 : 0), 0)
	);

	const remainingRightTokens = (
		props.ship.rightTokens
		- props.moves.reduce((total, move) => total + (move.token === MovementToken.Right ? 1 : 0), 0)
	);

	const remainingCannons = (
		props.ship.loadedCannons
		- props.moves.reduce((total, move) => total + (move.fire?.left ? 1 : 0) + (move.fire?.right ? 1 : 0), 0)
	);

	const hull = (
		props.ship.type === ShipType.Sloop ? 60 :
		props.ship.type === ShipType.Brig ? 90 :
		props.ship.type === ShipType.Galleon ? 120 :
		props.ship.type === ShipType.Frigate ? 150 :
		1 // ???
	);

	const spritesheet = (
		props.ship.type === ShipType.Sloop ? SloopSpritesheet :
		props.ship.type === ShipType.Brig ? BrigSpritesheet :
		props.ship.type === ShipType.Galleon ? GalleonSpritesheet :
		props.ship.type === ShipType.Frigate ? FrigateSpritesheet :
		SloopSpritesheet // ???
	);

	const haloSpritesheet = (
		props.ship.type === ShipType.Sloop ? SloopHaloSpritesheet :
		props.ship.type === ShipType.Brig ? BrigHaloSpritesheet :
		props.ship.type === ShipType.Galleon ? GalleonHaloSpritesheet :
		props.ship.type === ShipType.Frigate ? FrigateHaloSpritesheet :
		SloopHaloSpritesheet // ???
	);

	const frames = (
		props.ship.type === ShipType.Sloop ? SloopFrames :
		props.ship.type === ShipType.Brig ? BrigFrames :
		props.ship.type === ShipType.Galleon ? GalleonFrames :
		props.ship.type === ShipType.Frigate ? FrigateFrames :
		SloopFrames // ???
	);

	return (
		<div
			className={classes(styles.shipControls, props.className)}
			onDragOver={(event) => {
				event.preventDefault();
				event.dataTransfer.dropEffect = "link";
			}}
			onDrop={(event) => {
				event.preventDefault();
			}}
		>
			<div
				className={classes(
					styles.ship,
					props.ship.sunk ? styles.sunk : undefined,
				)}
			>
				<div
					className={styles.header}
					onMouseEnter={() => setHighlightTarget({ kind: "ship", id: props.ship.id })}
					onMouseLeave={() => setHighlightTarget(undefined)}
				>
					<div className={styles.icon}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={haloSpritesheet}
							frame={frames[Heading.South]}
							offset={new ScreenPoint(22.5, 32)}
						/>
						<Sprite
							className={styles.sprite}
							spritesheet={spritesheet}
							frame={frames[Heading.South]}
							offset={new ScreenPoint(22.5, 32)}
						/>
					</div>
					<OutlineText
						className={classes(
							styles.name,
							(
								props.ship.type === ShipType.Sloop ? styles.sloop :
								props.ship.type === ShipType.Brig ? styles.brig :
								props.ship.type === ShipType.Galleon ? styles.galleon :
								props.ship.type === ShipType.Frigate ? styles.frigate :
								undefined
							)
						)}
					>
						{props.ship.name + (props.ship.sunk ? " <Sunk>" : "")}
					</OutlineText>
				</div>
				<div className={styles.damage}>
					<div
						className={styles.damageFilled}
						style={{
							width: `${(props.ship.damage / hull) * 100}%`,
						}}
					/>
				</div>
				<div className={styles.cannonballs}>
					Cannonballs x{props.ship.cannonballs}
				</div>
			</div>
			<div className={styles.tokens}>
				<div className={styles.tokenPool}>
					<DraggableFireToken size="large" disabled={remainingCannons <= 0} dragsetId={instanceId} />
					<div className={styles.count}>x{remainingCannons}</div>
				</div>
				<div className={styles.tokenPool}>
					<DraggableToken
						kind={MovementToken.Forward}
						disabled={remainingForwardTokens <= 0}
						dragsetId={instanceId}
					/>
					<div className={styles.count}>x{remainingForwardTokens}</div>
				</div>
				<div className={styles.tokenPool}>
					<DraggableToken
						kind={MovementToken.Left}
						disabled={remainingLeftTokens <= 0}
						dragsetId={instanceId}
					/>
					<div className={styles.count}>x{remainingLeftTokens}</div>
				</div>
				<div className={styles.tokenPool}>
					<DraggableToken
						kind={MovementToken.Right}
						disabled={remainingRightTokens <= 0}
						dragsetId={instanceId}
					/>
					<div className={styles.count}>x{remainingRightTokens}</div>
				</div>
			</div>
			<div className={styles.moves}>
				{
					Array.from(new Array(4), (_, i) => (
						<div key={i} className={styles.move}>
							<div
								className={classes(
									styles.fire,
									styles.left,
								)}
								onClick={() => {
									if (remainingCannons <= 0 && !props.moves[i].fire?.left) {
										return;
									}

									const newMoves = (
										props.moves.map((move) => Move.clone(move)) as [Move, Move, Move, Move]
									);
									newMoves[i].fire = {
										...newMoves[i].fire,
										left: !newMoves[i].fire?.left
									};
									props.onMovesChange(newMoves);
								}}
								onDragOver={(event) => {
									event.preventDefault();
									event.stopPropagation();

									event.dataTransfer.dropEffect = "move";
								}}
								onDrop={(event) => {
									event.preventDefault();
									event.stopPropagation();

									const newMoves = (
										props.moves.map((move) => Move.clone(move)) as [Move, Move, Move, Move]
									);
									const dragset = event.dataTransfer.getData("application/dragset");
									const token = event.dataTransfer.getData("application/fire-token");
									const source = event.dataTransfer.getData("application/token-source");

									if (token === "" || dragset !== instanceId) {
										return;
									}

									if (source !== "") {
										const sourceMove = Number(source.split(":")[0]);
										const sourceSide = source.split(":")[1];
										const currentToken = newMoves[i].fire?.left ?? false;
										newMoves[i].fire = { ...newMoves[i].fire, left: true };
										newMoves[sourceMove].fire = {
											...newMoves[sourceMove].fire,
											[sourceSide]: currentToken
										};
									} else {
										newMoves[i].fire = { ...newMoves[i].fire, left: true };
									}

									return props.onMovesChange(newMoves);
								}}
							>
								{
									props.moves[i].fire?.left
										? (
											<DraggableFireToken
												size="small"
												dragsetId={instanceId}
												onDragStart={(event) => {
													event.dataTransfer.setData("application/token-source", `${i}:left`);
												}}
												onDragEnd={(event) => {
													event.preventDefault();
													if (event.dataTransfer.dropEffect === "link") {
														const newMoves = (
															props.moves.map((move) => Move.clone(move))
														) as [Move, Move, Move, Move];
														newMoves[i].fire = { ...newMoves[i].fire, left: false };
														return props.onMovesChange(newMoves);
													}
												}}
											/>
										)
										: undefined
								}
							</div>
							<div
								className={styles.movement}
								onDragOver={(event) => {
									event.preventDefault();
									event.stopPropagation();

									event.dataTransfer.dropEffect = "move";
								}}
								onDrop={(event) => {
									event.preventDefault();
									event.stopPropagation();

									const newMoves = (
										props.moves.map((move) => Move.clone(move)) as [Move, Move, Move, Move]
									);
									const dragset = event.dataTransfer.getData("application/dragset");
									const token = (
										event.dataTransfer.getData("application/movement-token") as MovementToken | ""
									);
									const source = event.dataTransfer.getData("application/token-source");

									if (token === "" || dragset !== instanceId) {
										return;
									}

									if (source !== "") {
										const currentToken = newMoves[i].token;
										newMoves[i].token = token;
										newMoves[Number(source)].token = currentToken;
									} else {
										newMoves[i].token = token;
									}

									return props.onMovesChange(newMoves);
								}}
							>
								{
									props.moves[i].token !== undefined
										? (
											<DraggableToken
												kind={props.moves[i].token!}
												dragsetId={instanceId}
												onDragStart={(event) => {
													event.dataTransfer.setData(
														"application/token-source",
														i.toString()
													);
												}}
												onDragEnd={(event) => {
													event.preventDefault();
													if (event.dataTransfer.dropEffect === "link") {
														const newMoves = (
															props.moves.map((move) => Move.clone(move))
														) as [Move, Move, Move, Move];
														newMoves[i].token = undefined;
														return props.onMovesChange(newMoves);
													}
												}}
												onDoubleClick={() => {
													const newMoves = (
														props.moves.map((move) => Move.clone(move))
													) as [Move, Move, Move, Move];
													newMoves[i].token = undefined;
													return props.onMovesChange(newMoves);
												}}
											/>
										)
										: undefined
								}
							</div>
							<div
								className={classes(
									styles.fire,
									styles.right,
								)}
								onClick={() => {
									if (remainingCannons <= 0 && !props.moves[i].fire?.right) {
										return;
									}

									const newMoves = (
										props.moves.map((move) => Move.clone(move)) as [Move, Move, Move, Move]
									);
									newMoves[i].fire = {
										...newMoves[i].fire,
										right: !newMoves[i].fire?.right
									};
									props.onMovesChange(newMoves);
								}}
								onDragOver={(event) => {
									event.preventDefault();
									event.stopPropagation();

									event.dataTransfer.dropEffect = "move";
								}}
								onDrop={(event) => {
									event.preventDefault();
									event.stopPropagation();

									const newMoves = (
										props.moves.map((move) => Move.clone(move)) as [Move, Move, Move, Move]
									);
									const dragset = event.dataTransfer.getData("application/dragset");
									const token = event.dataTransfer.getData("application/fire-token");
									const source = event.dataTransfer.getData("application/token-source");

									if (token === "" || dragset !== instanceId) {
										return;
									}

									if (source !== "") {
										const sourceMove = Number(source.split(":")[0]);
										const sourceSide = source.split(":")[1];
										const currentToken = newMoves[i].fire?.right ?? false;
										newMoves[i].fire = { ...newMoves[i].fire, right: true };
										newMoves[sourceMove].fire = {
											...newMoves[sourceMove].fire,
											[sourceSide]: currentToken
										};
									} else {
										newMoves[i].fire = { ...newMoves[i].fire, right: true };
									}

									return props.onMovesChange(newMoves);
								}}
							>
								{
									props.moves[i].fire?.right
										? (
											<DraggableFireToken
												size="small"
												dragsetId={instanceId}
												onDragStart={(event) => {
													event.dataTransfer.setData(
														"application/token-source",
														`${i}:right`
													);
												}}
												onDragEnd={(event) => {
													event.preventDefault();
													if (event.dataTransfer.dropEffect === "link") {
														const newMoves = (
															props.moves.map((move) => Move.clone(move))
														) as [Move, Move, Move, Move];
														newMoves[i].fire = { ...newMoves[i].fire, right: false };
														return props.onMovesChange(newMoves);
													}
												}}
											/>
										)
										: undefined
								}
							</div>
						</div>
					))
				}
			</div>
		</div>
	);
};

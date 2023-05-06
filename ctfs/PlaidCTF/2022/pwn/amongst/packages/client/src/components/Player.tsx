import React from "react";

import { Color, Direction, PlayerVisualState } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import Shadow from "/assets/shadow.png";
import SpritesheetJson from "/assets/shipmate-spritesheet.json";
import Spritesheet from "/assets/shipmate-spritesheet.png";

import { useColorFilter } from "../hooks/useColorFilter";
import { usePartialTick } from "../hooks/usePartialTick";
import { usePrevious } from "../hooks/usePrevious";
import { PixelsPerUnit } from "../utils/constants";
import { classes } from "../utils/css";
import { Anchor, Frame, Sprite } from "./Sprite";

import styles from "./Player.module.scss";

interface Props {
	tick: number;
	name: string;
	color: Color;
	location: Point;
	visualState: PlayerVisualState;
	dead?: boolean;
	hoaxer?: boolean;
}

const PlayerIntl = (props: Props) => {
	const colorFilter = useColorFilter(props.color);

	const frameName = (
		props.visualState.kind === PlayerVisualState.Kind.Idle ?
			"idle" :
		props.visualState.kind === PlayerVisualState.Kind.Moving ?
			SpritesheetJson.animations.walk[props.visualState.frame] :
		""
	);

	const frameData = (SpritesheetJson.frames as Record<string, { frame: Frame; anchor: Anchor }>)[frameName];

	return (
		<div className={styles.player}>
			<Sprite
				url={Spritesheet}
				frame={frameData.frame}
				anchor={frameData.anchor}
				position={props.location}
				opacity={props.dead ? 0.5 : 1}
				flipX={props.visualState.direction === Direction.Left}
				filter={colorFilter}
			/>
			<Sprite
				url={Shadow}
				frame={{ x: 0, y: 0, w: 60, h: 30 }}
				anchor={{ x: 30, y: 15 }}
				position={props.location}
				opacity={1}
			/>
			<div
				className={classes(
					styles.name,
					props.hoaxer ? styles.hoaxer : undefined,
				)}
				style={{
					left: props.location.x * PixelsPerUnit,
					top: props.location.y * PixelsPerUnit - 100,
					transform: "translate(-50%, -50%)"
				}}
			>
				{props.name}
			</div>
		</div>
	);
};

const Self = (props: Props) => (
	<PlayerIntl
		tick={props.tick}
		name={props.name}
		color={props.color}
		location={props.location}
		visualState={props.visualState}
		dead={props.dead}
		hoaxer={props.hoaxer}
	/>
);

const Other = (props: Props) => {
	const previousLocation = usePrevious(props.tick, props.location, props.location);
	const partialTick = usePartialTick();
	const location = previousLocation.scale(1 - partialTick).add(props.location.scale(partialTick));

	return (
		<PlayerIntl
			tick={props.tick}
			name={props.name}
			color={props.color}
			location={location}
			visualState={props.visualState}
			dead={props.dead}
			hoaxer={props.hoaxer}
		/>
	);
};

export const Player = { Self, Other };

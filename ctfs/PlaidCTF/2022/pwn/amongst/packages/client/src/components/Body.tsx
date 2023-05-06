import React from "react";

import { Color } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import SpritesheetJson from "/assets/shipmate-spritesheet.json";
import Spritesheet from "/assets/shipmate-spritesheet.png";

import { useColorFilter } from "../hooks/useColorFilter";
import { Anchor, Frame, Sprite } from "./Sprite";

import styles from "./Body.module.scss";

interface Props {
	color: Color;
	location: Point;
}

export const Body = (props: Props) => {
	const colorFilter = useColorFilter(props.color);

	const frameData: { frame: Frame; anchor: Anchor } = SpritesheetJson.frames.idle;

	return (
		<div className={styles.body}>
			<Sprite
				url={Spritesheet}
				frame={frameData.frame}
				anchor={frameData.anchor}
				position={props.location}
				rotation={Math.PI / 2}
				filter={colorFilter}
			/>
		</div>
	);
};

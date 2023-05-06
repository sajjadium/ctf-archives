import React from "react";

import { Point as GamePoint } from "@puzzled/types";

import { useGameToScreenMapper } from "@/hooks/useGameToScrenMapper.js";
import { classes } from "@/utils/css.js";

import styles from "./InfluenceZone.module.scss";

interface Props {
	className?: string;
	radius: number;
}

export const InfluenceZone = (props: Props) => {
	const gameToScreenMapper = useGameToScreenMapper();
	const delta = gameToScreenMapper(new GamePoint(1, 0)).subtract(gameToScreenMapper(new GamePoint(0, 0)));

	return (
		<div
			className={classes(styles.influenceZone, props.className)}
			style={{
				width: props.radius * 2 * Math.sqrt(2) * Math.abs(delta.x) + Number(styles.borderThickness),
				height: props.radius * 2 * Math.sqrt(2) * Math.abs(delta.x) + Number(styles.borderThickness),
				transform: `translate(-50%, -50%) scaleY(${Math.abs(delta.y) / Math.abs(delta.x)})`
			}}
		/>
	);
};

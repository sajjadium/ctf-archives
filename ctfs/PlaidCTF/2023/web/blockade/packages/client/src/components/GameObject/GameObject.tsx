import React from "react";

import { Point as GamePoint } from "@puzzled/types";

import { useGameToScreenMapper } from "@/hooks/useGameToScrenMapper.js";
import { classes } from "@/utils/css.js";

import styles from "./GameObject.module.scss";

interface Props {
	className?: string;
	children: React.ReactNode;
	location: GamePoint;
	layer?: number;
	onMouseEnter?: () => void;
	onMouseLeave?: () => void;
}

export const GameObject = (props: Props) => {
	const screenPoint = useGameToScreenMapper()(props.location);

	return (
		<div
			className={classes(styles.gameObject, props.className)}
			style={{
				transform: `translate(${screenPoint.x}px, ${screenPoint.y}px)`,
				zIndex: screenPoint.y + 10000 * (props.layer ?? 1)
			}}
			onMouseEnter={props.onMouseEnter}
			onMouseLeave={props.onMouseLeave}
		>
			{props.children}
		</div>
	);
};

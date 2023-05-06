import React from "react";

import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import styles from "./Point.module.scss";

interface Props {
	className?: string;
	offset?: ScreenPoint;
}

export const Point = (props: Props) => (
	<div
		className={classes(styles.point, props.className)}
		style={{
			left: props.offset?.x ?? 0,
			top: props.offset?.y ?? 0,
		}}
	/>
);

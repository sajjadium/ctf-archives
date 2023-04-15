import React from "react";

import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import styles from "./Text.module.scss";

interface Props {
	className?: string;
	children: string;
	offset?: ScreenPoint;
	align?: "left" | "center" | "right";
}

export const Text = (props: Props) => (
	<div
		className={classes(styles.text, props.className)}
		style={{
			left: props.offset?.x ?? 0,
			top: props.offset?.y ?? 0,
			textAlign: props.align ?? "left",
			transform: (
				props.align === "center" ? "translate(-50%, 0)" :
				props.align === "right" ? "translate(-100%, 0)" :
				""
			)
		}}
	>
		<div className={styles.outline}>{props.children}</div>
		<div className={styles.fill}>{props.children}</div>
	</div>
);


import React from "react";

import { classes } from "@/utils/css.js";

import styles from "./DraggableFireToken.module.scss";

interface Props {
	size: "large" | "small";
	disabled?: boolean;
	onDragStart?: (event: React.DragEvent<HTMLDivElement>) => void;
	onDragEnd?: (event: React.DragEvent<HTMLDivElement>) => void;
	dragsetId: string;
}

export const DraggableFireToken = (props: Props) => (
	<div
		className={classes(
			styles.draggableFireToken,
			(
				props.size === "large" ? styles.large :
				props.size === "small" ? styles.small :
				undefined
			),
			props.disabled ? styles.disabled : undefined
		)}
		draggable={!props.disabled}
		onDragStart={(event) => {
			event.dataTransfer.setData("application/dragset", props.dragsetId);
			event.dataTransfer.setData("application/fire-token", "1");
			props.onDragStart?.(event);
		}}
		onDragEnd={(event) => {
			props.onDragEnd?.(event);
		}}
	/>
);

import React from "react";

import { MovementToken } from "@puzzled/types";

import { classes } from "@/utils/css.js";

import { Token } from "../Token/index.js";

import styles from "./DraggableToken.module.scss";

interface Props {
	kind: MovementToken;
	disabled?: boolean;
	onDragStart?: (event: React.DragEvent<HTMLDivElement>) => void;
	onDragEnd?: (event: React.DragEvent<HTMLDivElement>) => void;
	onDoubleClick?: (event: React.MouseEvent<HTMLDivElement>) => void;
	dragsetId: string;
}

export const DraggableToken = (props: Props) => (
	<div
		className={classes(
			styles.draggableToken,
			props.disabled ? styles.disabled : undefined
		)}
		draggable={!props.disabled}
		onDragStart={(event) => {
			event.dataTransfer.setData("application/dragset", props.dragsetId);
			event.dataTransfer.setData("application/movement-token", props.kind);
			props.onDragStart?.(event);
		}}
		onDragEnd={(event) => {
			props.onDragEnd?.(event);
		}}
		onDoubleClick={props.onDoubleClick}
	>
		<Token kind={props.kind} />
	</div>
);

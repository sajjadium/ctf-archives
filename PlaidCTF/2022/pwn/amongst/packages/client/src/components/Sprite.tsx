import React from "react";

import { Point } from "@amongst/geometry";

import { PixelsPerUnit } from "../utils/constants";

import styles from "./Sprite.module.scss";

export interface Frame {
	x: number;
	y: number;
	w: number;
	h: number;
}

export interface Anchor {
	x: number;
	y: number;
}

export interface Props {
	url: string;
	frame: Frame;
	anchor?: Anchor;
	position: Point;
	flipX?: boolean;
	filter?: string;
	opacity?: number;
	rotation?: number;
	layer?: number;
	scale?: number;
}

export const Sprite = (props: Props) => (
	<div
		className={styles.sprite}
		style={{
			left: props.position.x * PixelsPerUnit,
			top: props.position.y * PixelsPerUnit,
			zIndex: Math.round(((props.layer ?? 0) * 1000) + 10000 + props.position.y * 100)
		}}
	>
		<div
			className={styles.image}
			style={{
				backgroundImage: `url(${props.url})`,
				backgroundPosition: `${-props.frame.x}px ${-props.frame.y}px`,
				backgroundRepeat: "no-repeat",
				width: props.frame.w,
				height: props.frame.h,
				transform: `
					translate(${-(props.anchor?.x ?? 0)}px, ${-(props.anchor?.y ?? 0)}px)
					rotate(${props.rotation ?? 0}rad)
					scale(${props.scale ?? 1})
					scaleX(${props.flipX ? -1 : 1})
				`,
				transformOrigin: `${props.anchor?.x ?? 0}px ${props.anchor?.y ?? 0}px`,
				filter: props.filter,
				opacity: props.opacity
			}}
		/>
	</div>
);

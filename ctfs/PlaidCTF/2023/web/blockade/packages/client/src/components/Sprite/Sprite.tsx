import React from "react";

import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import styles from "./Sprite.module.scss";

interface Props {
	className?: string;
	offset?: ScreenPoint;
	spritesheet: {
		url: string;
		size: ScreenPoint; // after scaling
	};
	frame: {
		offset: ScreenPoint;
		size: ScreenPoint;
		anchor: ScreenPoint;
	};
	mask?: boolean;
}

export const Sprite = (props: Props) => {
	const imageProps = (
		props.mask
			? {
				maskImage: `url(${props.spritesheet.url})`,
				maskSize: `${props.spritesheet.size.x}px ${props.spritesheet.size.y}px`,
				maskPosition: `-${props.frame.offset.x}px -${props.frame.offset.y}px`,
				WebkitMaskImage: `url(${props.spritesheet.url})`,
				WebkitMaskSize: `${props.spritesheet.size.x}px ${props.spritesheet.size.y}px`,
				WebkitMaskPosition: `-${props.frame.offset.x}px -${props.frame.offset.y}px`,
			}
			: {
				backgroundImage: `url(${props.spritesheet.url})`,
				backgroundSize: `${props.spritesheet.size.x}px ${props.spritesheet.size.y}px`,
				backgroundPosition: `-${props.frame.offset.x}px -${props.frame.offset.y}px`,
			}
	);

	return (
		<div
			className={classes(styles.sprite, props.className)}
			style={{
				left: props.offset?.x ?? 0,
				top: props.offset?.y ?? 0,
				width: props.frame.size.x,
				height: props.frame.size.y,
				...imageProps,
				transform: `translate(-${props.frame.anchor.x}px, -${props.frame.anchor.y}px)`
			}}
		/>
	);
};

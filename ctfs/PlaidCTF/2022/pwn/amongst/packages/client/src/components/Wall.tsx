import React from "react";

import { Wall as GameWall } from "@amongst/game-common";

import { useWallPattern } from "../hooks/useWallPattern";
import { PixelsPerUnit } from "../utils/constants";

import styles from "./Wall.module.scss";

const Padding = 10;

interface Props {
	wall: GameWall;
}

export const Wall = (props: Props) => {
	const pattern = useWallPattern();

	const box = props.wall.getBoundingBox();
	const scaledBox = box.scale(PixelsPerUnit);
	const width = scaledBox.bottomRight.x - scaledBox.topLeft.x + 2 * Padding;
	const height = scaledBox.bottomRight.y - scaledBox.topLeft.y + 2 * Padding;

	const start = props.wall.start.scale(PixelsPerUnit);
	const end = props.wall.end.scale(PixelsPerUnit);
	const length = end.sub(start).mag();

	return (
		<svg
			className={styles.wall}
			viewBox={`
				${scaledBox.topLeft.x - Padding} ${scaledBox.topLeft.y - Padding}
				${width} ${height}
			`}
			style={{
				left: scaledBox.topLeft.x - Padding,
				top: scaledBox.topLeft.y - Padding,
				width,
				height
			}}
		>
			<g
				style={{
					transform: `
						translate(${start.x}px, ${start.y}px)
						rotate(${end.sub(start).ang()}rad)
					`
				}}
			>
				<rect
					className={styles.background}
					x={0}
					y={-8}
					width={length}
					height={8}
				/>
				<rect
					className={styles.pattern}
					x={0}
					y={-8}
					width={length}
					height={8}
					style={{
						fill: `${pattern}`,
					}}
				/>
			</g>
		</svg>
	);
};

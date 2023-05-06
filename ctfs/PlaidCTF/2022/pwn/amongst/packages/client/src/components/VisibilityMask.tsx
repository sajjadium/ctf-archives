import React from "react";

import { Level as GameLevel } from "@amongst/game-client";
import { MapGraphics } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import { useUniqueId } from "../hooks/useUniqueId";
import { PixelsPerUnit } from "../utils/constants";

import styles from "./VisibilityMask.module.scss";

interface Props {
	disable?: boolean;
	level: GameLevel;
	graphics: MapGraphics;
	selfLocation: Point;
	children: React.ReactNode;
}

export const VisibilityMask = (props: Props) => {
	const lightPolygonId = useUniqueId("light-polygon");

	const lightLocation =(
		props.selfLocation.scale(PixelsPerUnit)
			.add(props.graphics.origin)
	);

	const gradientMask = `
		radial-gradient(
			circle at ${lightLocation.x}px ${lightLocation.y}px,
			rgba(0,0,0,1) ${props.graphics.visibility * 0.75 * PixelsPerUnit}px,
			rgba(0,0,0,0.9) ${props.graphics.visibility * 0.85 * PixelsPerUnit}px,
			rgba(0,0,0,0) ${props.graphics.visibility * PixelsPerUnit}px
		)
	`;

	const visibilityPolygon = (
		props.level.map.getVisiblityPolygon(props.selfLocation)
			.scale(PixelsPerUnit)
			.translate(props.graphics.origin)
	);

	const wallOffset = new Point(0, -3.6).scale(PixelsPerUnit);

	const clipStyle: React.CSSProperties = props.disable ? {} : {
		clipPath: `url(#${lightPolygonId})`,
		WebkitClipPath: `url(#${lightPolygonId})`,
		maskImage: gradientMask,
		WebkitMaskImage: gradientMask
	};

	return (
		<>
			<svg>
				<defs>
					<clipPath id={lightPolygonId}>
						<polygon
							fill="#000000"
							points={visibilityPolygon.toSvg()}
						/>
						{
							[...visibilityPolygon.edges()]
								.map(([a, b], i) => (
									<polygon
										key={i}
										fill="#ff0000"
										points={`
											${a.toSvg()}
											${b.toSvg()}
											${b.add(wallOffset).toSvg()}
											${a.add(wallOffset).toSvg()}
										`}
									/>
								))
						}
					</clipPath>
				</defs>
			</svg>
			<div
				className={styles.visibilityMask}
				style={{
					...clipStyle,
					transform: `translate(${-props.graphics.origin.x}px, ${-props.graphics.origin.y}px)`,
					width: (props.level.map.bounds.bottomRight.x - props.level.map.bounds.topLeft.x) * PixelsPerUnit,
					height: (props.level.map.bounds.bottomRight.y - props.level.map.bounds.topLeft.y) * PixelsPerUnit,
				}}
			>
				<div
					className={styles.content}
					style={{
						transform: `translate(${props.graphics.origin.x}px, ${props.graphics.origin.y}px)`,
					}}
				>
					{props.children}
				</div>
			</div>
		</>
	);
};

import React from "react";

import { Point as GamePoint } from "@puzzled/types";

import { GameObject } from "@/components/GameObject/index.js";
import { Sprite } from "@/components/Sprite/index.js";
import { Text } from "@/components/Text/index.js";
import { useHighlight } from "@/contexts/HighlightContext.js";
import { HalfHeading } from "@/types/HalfHeading.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import { InfluenceZone } from "../InfluenceZone/index.js";

import styles from "./Ship.module.scss";

interface Props {
	className?: string;
	id: number;
	name: string;
	faction: number;
	location: GamePoint;
	heading: HalfHeading;
	sunk: boolean;
	influence: number;
	shipSpritesheet: {
		url: string;
		size: ScreenPoint;
	};
	shipFrames: {
		[heading in HalfHeading]: {
			offset: ScreenPoint;
			size: ScreenPoint;
			anchor: ScreenPoint;
		};
	};
	haloSpritesheet: {
		url: string;
		size: ScreenPoint;
	};
	haloFrames: {
		[heading in HalfHeading]: {
			offset: ScreenPoint;
			size: ScreenPoint;
			anchor: ScreenPoint;
		};
	};
	nameOffset: ScreenPoint;
}

export const Ship = (props: Props) => {
	const [highlightTarget, setHighlightTarget] = useHighlight();
	const highlighted = (
		(highlightTarget?.kind === "ship" && highlightTarget.id === props.id)
		|| (highlightTarget?.kind === "faction" && highlightTarget.id === props.faction)
	);

	return (
		<div
			className={classes(
				styles.ship,
				styles[`faction${props.faction}`],
				props.sunk ? styles.sunk : undefined,
				props.className
			)}
		>
			<GameObject
				location={props.location}
				onMouseEnter={() => setHighlightTarget({ kind: "ship", id: props.id })}
				onMouseLeave={() => setHighlightTarget(undefined)}
			>
				<Sprite
					className={styles.halo}
					mask
					spritesheet={props.haloSpritesheet}
					frame={props.haloFrames[props.heading]}
				/>
				<Sprite
					className={styles.sprite}
					spritesheet={props.shipSpritesheet}
					frame={props.shipFrames[props.heading]}
				/>
				<Text
					className={styles.name}
					offset={props.nameOffset}
					align="center"
				>
					{props.name}
				</Text>
			</GameObject>
			{
				highlighted
					? (
						<GameObject
							location={props.location}
							layer={-1}
						>
							<InfluenceZone
								className={styles.influenceZone}
								radius={props.influence}
							/>
						</GameObject>
					)
					: null
			}
		</div>
	);
};

import React from "react";

import { Heading, Point as GamePoint } from "@puzzled/types";

import { ShipProps } from "@/components/Ship/index.js";
import { CannonFrames, CannonSpritesheet } from "@/spritesheets/Cannon.js";
import { HalfHeading } from "@/types/HalfHeading.js";

import { GameObject } from "../GameObject/index.js";
import { Sprite } from "../Sprite/Sprite.js";

interface Props {
	className?: string;
	ship: React.ComponentType<ShipProps>;
	progress: number;
	at: {
		location: GamePoint;
		heading: Heading;
	};
	move?: {
		to: {
			location: GamePoint;
			heading: Heading;
		};
		intent: {
			location: GamePoint;
			heading: Heading;
		};
	};
	fire?: {
		left?: {
			hit: boolean;
			to: GamePoint;
		};
		right?: {
			hit: boolean;
			to: GamePoint;
		};
	};
	info: {
		id: number;
		name: string;
		faction: number;
		sunk: boolean;
	};
}

export const ShipController = (props: Props) => {
	const from = props.at;
	const intent = props.move?.intent ?? props.at;
	const to = props.move?.to ?? props.at;

	let location: GamePoint;
	let heading: HalfHeading;

	if (intent.location.equals(from.location)) {
		// Ship didn't attempt to move
		location = from.location;
		heading = HalfHeading.fromHeading(from.heading);
	} else if (intent.location.equals(to.location)) {
		// Simple moves
		if (to.location.distanceTo(from.location) === 1) {
			// Move straight, possibly with rotation
			location = interpolatePoint([
				[0, from.location],
				[0.75, to.location]
			], props.progress);
			heading = (
				props.progress < 0.25 ? HalfHeading.fromHeading(from.heading) :
				props.progress < 0.5 ? HalfHeading.between(from.heading, to.heading) :
				HalfHeading.fromHeading(to.heading)
			);
		} else {
			// Turn with rotation
			location = interpolatePoint([
				[0, from.location],
				[0.3, from.location.add(Heading.toPoint(from.heading).scale(0.5))],
				[0.5, from.location.add(Heading.toPoint(from.heading).scale(0.854)).add(Heading.toPoint(to.heading).scale(0.146))],
				[0.7, to.location.subtract(Heading.toPoint(to.heading).scale(0.5))],
				[1, to.location]
			], props.progress);
			heading = (
				props.progress < 0.35 ? HalfHeading.fromHeading(from.heading) :
				props.progress < 0.65 ? HalfHeading.between(from.heading, to.heading) :
				HalfHeading.fromHeading(to.heading)
			);
		}
	} else if (to.location.equals(from.location)) {
		// Attempt move, but rebound, possibly with rotation
		if (intent.location.distanceTo(from.location) === 1) {
			// Attempted linear movement
			location = interpolatePoint([
				[0, from.location],
				[0.45, from.location.add(intent.location.subtract(from.location).scale(0.6))],
				[1, to.location]
			], props.progress);
			heading = (
				props.progress < 0.3 ? HalfHeading.fromHeading(from.heading) :
				props.progress < 0.45 ? HalfHeading.between(from.heading, to.heading) :
				HalfHeading.fromHeading(to.heading)
			);
		} else {
			// Attempted turn, but failed immediately
			location = interpolatePoint([
				[0, from.location],
				[0.45, from.location.add(Heading.toPoint(from.heading).scale(0.6))],
				[1, to.location]
			], props.progress);
			heading = (
				props.progress < 0.3 ? HalfHeading.fromHeading(from.heading) :
				props.progress < 0.45 ? HalfHeading.between(from.heading, to.heading) :
				HalfHeading.fromHeading(to.heading)
			);
		}
	} else {
		// Get halfway through a turn, then rebound
		location = interpolatePoint([
			[0, from.location],
			[0.3, from.location.add(Heading.toPoint(from.heading).scale(0.5))],
			[0.5, from.location.add(Heading.toPoint(from.heading).scale(0.854)).add(Heading.toPoint(to.heading).scale(0.146))],
			[0.7, intent.location.subtract(Heading.toPoint(intent.heading).scale(0.5))],
			[1, to.location]
		], props.progress);
		heading = (
			props.progress < 0.35 ? HalfHeading.fromHeading(from.heading) :
			props.progress < 0.65 ? HalfHeading.between(from.heading, to.heading) :
			HalfHeading.fromHeading(to.heading)
		);
	}

	let smoke: React.ReactNode | undefined;
	let leftCannon: React.ReactNode | undefined;
	let rightCannon: React.ReactNode | undefined;

	if (props.fire?.left !== undefined || props.fire?.right !== undefined) {
		smoke = (
			<GameObject location={location}>
				<Sprite
					spritesheet={CannonSpritesheet}
					frame={
						props.progress < 0.3 ? CannonFrames.smoke1 :
						props.progress < 0.6 ? CannonFrames.smoke2 :
						props.progress < 0.9 ? CannonFrames.smoke3 :
						CannonFrames.blank
					}
				/>
			</GameObject>
		);

		if (props.fire?.left !== undefined) {
			const travelTime = props.fire.left.to.distanceTo(location) * 0.25;

			if (props.progress < travelTime) {
				const cannonballLocation = interpolatePoint([
					[0, location],
					[travelTime, props.fire.left.to]
				], props.progress);

				leftCannon = (
					<GameObject location={cannonballLocation}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={CannonFrames.cannonball}
						/>
					</GameObject>
				);
			} else if (props.fire.left.hit) {
				leftCannon = (
					<GameObject location={props.fire.left.to}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={
								props.progress < travelTime + 0.3 ? CannonFrames.hit1 :
								props.progress < travelTime + 0.6 ? CannonFrames.hit2 :
								props.progress < travelTime + 0.9 ? CannonFrames.hit3 :
								props.progress < travelTime + 1.2 ? CannonFrames.hit4 :
								CannonFrames.blank
							}
						/>
					</GameObject>
				);
			} else {
				leftCannon = (
					<GameObject location={props.fire.left.to}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={
								props.progress < travelTime + 0.3 ? CannonFrames.splash1 :
								props.progress < travelTime + 0.6 ? CannonFrames.splash2 :
								props.progress < travelTime + 0.9 ? CannonFrames.splash3 :
								props.progress < travelTime + 1.2 ? CannonFrames.splash4 :
								CannonFrames.blank
							}
						/>
					</GameObject>
				);
			}
		}

		if (props.fire?.right !== undefined) {
			const travelTime = props.fire.right.to.distanceTo(location) * 0.2;

			if (props.progress < travelTime) {
				const cannonballLocation = interpolatePoint([
					[0, location],
					[travelTime, props.fire.right.to]
				], props.progress);

				rightCannon = (
					<GameObject location={cannonballLocation}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={CannonFrames.cannonball}
						/>
					</GameObject>
				);
			} else if (props.fire.right.hit) {
				rightCannon = (
					<GameObject location={props.fire.right.to}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={
								props.progress < travelTime + 0.3 ? CannonFrames.hit1 :
								props.progress < travelTime + 0.6 ? CannonFrames.hit2 :
								props.progress < travelTime + 0.9 ? CannonFrames.hit3 :
								props.progress < travelTime + 1.2 ? CannonFrames.hit4 :
								CannonFrames.blank
							}
						/>
					</GameObject>
				);
			} else {
				rightCannon = (
					<GameObject location={props.fire.right.to}>
						<Sprite
							spritesheet={CannonSpritesheet}
							frame={
								props.progress < travelTime + 0.3 ? CannonFrames.splash1 :
								props.progress < travelTime + 0.6 ? CannonFrames.splash2 :
								props.progress < travelTime + 0.9 ? CannonFrames.splash3 :
								props.progress < travelTime + 1.2 ? CannonFrames.splash4 :
								CannonFrames.blank
							}
						/>
					</GameObject>
				);
			}
		}
	}

	return (
		<>
			<props.ship
				className={props.className}
				location={location}
				heading={heading}
				{...props.info}
			/>
			{smoke}
			{leftCannon}
			{rightCannon}
		</>
	);
};

function interpolatePoint(keyframes: [number, GamePoint][], progress: number): GamePoint {
	for (let i = 0; i < keyframes.length; i++) {
		if (i === keyframes.length - 1) {
			return keyframes[i][1];
		} else if (progress < keyframes[i + 1][0]) {
			const [t0, p0] = keyframes[i];
			const [t1, p1] = keyframes[i + 1];
			const t = (progress - t0) / (t1 - t0);
			return p0.scale(1 - t).add(p1.scale(t));
		}
	}

	throw new Error("Invalid interpolation");
}

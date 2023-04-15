import { And, EntityManager, FindOperator, Not } from "typeorm";

import {
	FirePhaseResult,
	FireResult,
	Heading,
	Move,
	MovementPhaseResult,
	MovementToken,
	MoveOutcome
} from "@puzzled/types";

import { Buoy } from "../entities/Buoy.mjs";
import { Faction } from "../entities/Faction.mjs";
import { Gust } from "../entities/Gust.mjs";
import { Rock } from "../entities/Rock.mjs";
import { Ship } from "../entities/Ship.mjs";
import { Whirlpool } from "../entities/Whirlpool.mjs";
import {
	DistanceLessThanOrEqualTo,
	EqualsPoint,
	HorizontallyAlignedWith,
	StrictlyAbove,
	StrictlyBelow,
	StrictlyLeftOf,
	StrictlyRightOf,
	VerticallyAlignedWith
} from "../predicates.mjs";
import { MapHeight, MapWidth, MovementWearDamage } from "./constants.mjs";

export async function executeMove(tx: EntityManager, ship: Ship, move: Move): Promise<MoveOutcome> {
	const startLocation = ship.location;

	// Controlled move
	let controlledMoveResult: MovementPhaseResult;

	if (move.token !== undefined) {
		let intent = ship.location;
		consumeMovementToken(ship, move.token);

		const firstMoveSuccess = await moveShip(tx, ship, ship.heading);
		intent = intent.add(Heading.toPoint(ship.heading));
		ship.damage += MovementWearDamage;

		switch (move.token) {
			case MovementToken.Forward: break;

			case MovementToken.Left: {
				ship.heading = Heading.leftOf(ship.heading);
				break;
			}

			case MovementToken.Right: {
				ship.heading = Heading.rightOf(ship.heading);
				break;
			}
		}

		if (move.token !== MovementToken.Forward) {
			intent = intent.add(Heading.toPoint(ship.heading));

			if (firstMoveSuccess) {
				await moveShip(tx, ship, ship.heading);
			}
		}

		controlledMoveResult = {
			intent: {
				location: intent,
				heading: ship.heading
			},
			result: {
				location: ship.location,
				heading: ship.heading
			}
		};
	} else {
		controlledMoveResult = {
			intent: {
				location: ship.location,
				heading: ship.heading
			},
			result: {
				location: ship.location,
				heading: ship.heading
			}
		};
	}

	// Uncontrolled move
	let uncontrolledMoveResult = await interactWithGusts(tx, ship);

	if (uncontrolledMoveResult === undefined) {
		uncontrolledMoveResult = await interactWithWhirlpools(tx, ship);
	}

	if (uncontrolledMoveResult === undefined) {
		uncontrolledMoveResult = {
			intent: {
				location: ship.location,
				heading: ship.heading
			},
			result: {
				location: ship.location,
				heading: ship.heading
			}
		};
	}

	// Fire
	const fireResult: FirePhaseResult = {};

	if (move.fire?.left) {
		ship.loadedCannons--;

		if (ship.loadedCannons < 0) {
			throw new Error("Ship has no loaded cannons");
		}

		fireResult.left = await fire(tx, ship, Heading.leftOf(ship.heading));
	}

	if (move.fire?.right) {
		ship.loadedCannons--;

		if (ship.loadedCannons < 0) {
			throw new Error("Ship has no loaded cannons");
		}

		fireResult.right = await fire(tx, ship, Heading.rightOf(ship.heading));
	}

	// Save
	await tx.save(ship);

	// Score
	const oldScoringBuoys = await tx.find(Buoy, {
		where: {
			location: DistanceLessThanOrEqualTo(startLocation, ship.typeInfo.influenceRadius)
		}
	});

	const currentScoringBuoys = await tx.find(Buoy, {
		where: {
			location: DistanceLessThanOrEqualTo(ship.location, ship.typeInfo.influenceRadius)
		}
	});

	const oldScoringBuoyIds = new Set(oldScoringBuoys.map((buoy) => buoy.id));
	const turnScore = (
		currentScoringBuoys.reduce(
			(acc, buoy) => acc + (oldScoringBuoyIds.has(buoy.id) ? 1 : 2) * buoy.value,
			0
		)
	);

	await (
		tx.getRepository(Faction)
			.update(
				{
					id: ship.faction.id,
				}, {
					score: () => `score + ${turnScore}`
				}
			)
	);

	return {
		controlledMove: controlledMoveResult,
		uncontrolledMove: uncontrolledMoveResult,
		fire: fireResult
	};
}

function consumeMovementToken(ship: Ship, token: MovementToken) {
	switch (token) {
		case MovementToken.Forward: {
			ship.forwardTokens--;

			if (ship.forwardTokens < 0) {
				throw new Error("Ship has no forward tokens");
			}

			break;
		}

		case MovementToken.Left: {
			ship.leftTokens--;

			if (ship.leftTokens < 0) {
				throw new Error("Ship has no left tokens");
			}

			break;
		}

		case MovementToken.Right: {
			ship.rightTokens--;

			if (ship.rightTokens < 0) {
				throw new Error("Ship has no right tokens");
			}

			break;
		}
	}
}

async function moveShip(tx: EntityManager, ship: Ship, direction: Heading): Promise<boolean> {
	const newLocation = ship.location.add(Heading.toPoint(direction));

	const newLocationIsOutOfBounds = (
		newLocation.x < 0
		|| newLocation.x >= MapWidth
		|| newLocation.y < 0
		|| newLocation.y >= MapHeight
	);

	if (newLocationIsOutOfBounds) {
		ship.damage += ship.typeInfo.rockDamage;
		return false;
	}

	const newLocationHasRock = await tx.exists(Rock, {
		where: {
			location: EqualsPoint(newLocation)
		}
	});

	if (newLocationHasRock) {
		ship.damage += ship.typeInfo.rockDamage;
		return false;
	}

	const newLocationShip = await tx.findOne(Ship, {
		where: {
			location: EqualsPoint(newLocation),
			factionId: Not(ship.factionId),
			sunk: false
		},
		order: {
			id: "ASC"
		}
	});

	if (newLocationShip !== null) {
		ship.damage += newLocationShip.typeInfo.ramDamage;
		await tx.update(Ship, { id: newLocationShip.id }, {
			damage: () => `damage + ${ship.typeInfo.ramDamage}`
		});
		return false;
	}

	ship.location = newLocation;
	return true;
}

async function interactWithGusts(tx: EntityManager, ship: Ship): Promise<MovementPhaseResult | undefined> {
	const gust = await tx.findOneBy(Gust, {
		location: EqualsPoint(ship.location),
	});

	if (gust === null) {
		return undefined;
	}

	const intent = ship.location.add(Heading.toPoint(gust.heading));
	await moveShip(tx, ship, gust.heading);
	return {
		intent: {
			location: intent,
			heading: ship.heading
		},
		result: {
			location: ship.location,
			heading: ship.heading
		}
	};
}

async function interactWithWhirlpools(tx: EntityManager, ship: Ship): Promise<MovementPhaseResult | undefined> {
	const whirlpool = await tx.findOneBy(Whirlpool, {
		location: DistanceLessThanOrEqualTo(ship.location, 1),
	});

	if (whirlpool === null) {
		return undefined;
	}

	if (whirlpool.clockwise) {
		ship.location = (
			whirlpool.location
				.add(ship.location.subtract(whirlpool.location).rotateClockwise())
				.toInts()
		);
		ship.heading = Heading.rightOf(ship.heading);
	} else {
		ship.location = (
			whirlpool.location
				.add(ship.location.subtract(whirlpool.location).rotateCounterClockwise())
				.toInts()
		);
		ship.heading = Heading.leftOf(ship.heading);
	}

	return {
		intent: {
			location: ship.location,
			heading: ship.heading
		},
		result: {
			location: ship.location,
			heading: ship.heading
		}
	};
}

async function fire(tx: EntityManager, ship: Ship, direction: Heading): Promise<FireResult> {
	let alignmentCondition: FindOperator<any>;
	let directionCondition: FindOperator<any>;

	switch (direction) {
		case Heading.North: {
			alignmentCondition = VerticallyAlignedWith(ship.location);
			directionCondition = StrictlyAbove(ship.location);
			break;
		}

		case Heading.East: {
			alignmentCondition = HorizontallyAlignedWith(ship.location);
			directionCondition = StrictlyRightOf(ship.location);
			break;
		}

		case Heading.South: {
			alignmentCondition = VerticallyAlignedWith(ship.location);
			directionCondition = StrictlyBelow(ship.location);
			break;
		}

		case Heading.West: {
			alignmentCondition = HorizontallyAlignedWith(ship.location);
			directionCondition = StrictlyLeftOf(ship.location);
			break;
		}

		default: {
			throw new Error(`Invalid direction: ${direction as string}`);
		}
	}

	const possibleTargets = await tx.findBy(Ship, {
		location: And(
			alignmentCondition,
			directionCondition,
			DistanceLessThanOrEqualTo(ship.location, 3),
		),
		factionId: Not(ship.faction.id),
		sunk: false
	});

	if (possibleTargets.length === 0) {
		return { kind: "miss" };
	}

	const target = possibleTargets.reduce(
		(currentTarget, possibleTarget) => {
			const possibleDistance = ship.location.distanceTo(possibleTarget.location);
			const currentDistance = ship.location.distanceTo(currentTarget.location);
			if (possibleDistance < currentDistance) {
				return possibleTarget;
			} else if (possibleDistance === currentDistance && possibleTarget.id < currentTarget.id) {
				return possibleTarget;
			} else {
				return currentTarget;
			}
		},
		possibleTargets[0]
	);

	await tx.update(Ship, { id: target.id }, {
		damage: () => `damage + ${ship.typeInfo.cannonDamage}`
	});

	return { kind: "hit", location: target.location };
}

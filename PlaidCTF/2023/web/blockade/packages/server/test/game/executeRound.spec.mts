/* eslint-disable @typescript-eslint/no-unused-vars, max-len */

import { expect } from "chai";
import { Map } from "immutable";
import { describe } from "mocha";

import { FactionRoundMoves,Heading, MovementToken, Point, ShipRoundMoves } from "@puzzled/types";

import { dataSource } from "../../src/dataSource.mjs";
import { Ship } from "../../src/entities/Ship.mjs";
import { executeRound } from "../../src/game/executeRound.mjs";
import { createFaction, createShip } from "../../src/setupHelpers.mjs";

describe("executeRound", () => {
	before(async () => {
		await dataSource.initialize();
	});

	beforeEach(async () => {
		await dataSource.dropDatabase();
		await dataSource.synchronize();
	});

	after(async () => {
		await dataSource.destroy();
	});

	it("moves should be executed for each faction in the specified order", async () => {
		const faction1 = await createFaction({ name: "Test Faction 1" });
		const faction2 = await createFaction({ name: "Test Faction 2" });
		const ship1 = await createShip({
			faction: faction1,
			location: new Point(3, 4),
			heading: Heading.West,
			forwardTokens: 4,
			leftTokens: 4,
			rightTokens: 4,
			loadedCannons: 4
		});
		const ship2 = await createShip({
			faction: faction2,
			location: new Point(2, 3),
			heading: Heading.North,
			forwardTokens: 4,
			leftTokens: 4,
			rightTokens: 4,
			loadedCannons: 4
		});

		const moves = Map<number, FactionRoundMoves>([
			[
				faction1.id,
				Map<number, ShipRoundMoves>([
					[
						ship1.id,
						[
							{ token: MovementToken.Forward, fire: { right: true } },
							{ token: MovementToken.Right, fire: { right: true } },
							{ token: MovementToken.Forward },
							{ token: MovementToken.Right },
						]
					]
				])
			],
			[
				faction2.id,
				Map<number, ShipRoundMoves>([
					[
						ship2.id,
						[
							{ token: MovementToken.Right, fire: { right: true } },
							{ token: MovementToken.Right, fire: { right: true } },
							{ fire: { right: true } },
							{ token: MovementToken.Left }
						]
					]
				])
			]
		]);

		await executeRound(moves, [faction2.id, faction1.id]);

		const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
		const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });

		expect(foundShip1.location.x).to.equal(2);
		expect(foundShip1.location.y).to.equal(1);
		expect(foundShip1.heading).to.equal(Heading.East);
		expect(foundShip1.damage).to.equal(26);
		expect(foundShip1.loadedCannons).to.equal(3);

		expect(foundShip2.location.x).to.equal(5);
		expect(foundShip2.location.y).to.equal(4);
		expect(foundShip2.heading).to.equal(Heading.East);
		expect(foundShip2.damage).to.equal(10);
		expect(foundShip2.loadedCannons).to.equal(2);
	});

	it("a ship that sinks mid-round should not take further moves", async () => {
		const faction1 = await createFaction({ name: "Test Faction 1" });
		const faction2 = await createFaction({ name: "Test Faction 2" });
		const ship1 = await createShip({
			faction: faction1,
			location: new Point(1, 1),
			heading: Heading.North,
			damage: 75,
			forwardTokens: 4,
			leftTokens: 4,
			rightTokens: 4,
			loadedCannons: 4
		});
		const ship2 = await createShip({
			faction: faction2,
			location: new Point(2, 1),
			heading: Heading.North,
			forwardTokens: 4,
			leftTokens: 4,
			rightTokens: 4,
			loadedCannons: 4
		});

		const moves = Map<number, FactionRoundMoves>([
			[
				faction1.id,
				Map<number, ShipRoundMoves>([
					[
						ship1.id,
						[
							{ fire: { right: true } },
							{ fire: { right: true } },
							{ fire: { right: true } },
							{ fire: { right: true } }
						]
					]
				])
			],
			[
				faction2.id,
				Map<number, ShipRoundMoves>([
					[
						ship2.id,
						[
							{ fire: { left: true } },
							{ fire: { left: true } },
							{ fire: { left: true } },
							{ fire: { left: true } }
						]
					]
				])
			]
		]);

		await executeRound(moves, [faction1.id, faction2.id]);

		const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
		const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });

		expect(foundShip1.sunk).to.be.true;
		expect(foundShip2.damage).to.equal(7); // should only take the first shot
	});
});

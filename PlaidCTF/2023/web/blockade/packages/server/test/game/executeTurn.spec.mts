/* eslint-disable @typescript-eslint/no-unused-vars, max-len */

import { expect } from "chai";
import { Map } from "immutable";
import { describe } from "mocha";

import { Heading, MovementToken, Point } from "@puzzled/types";

import { dataSource } from "../../src/dataSource.mjs";
import { Ship } from "../../src/entities/Ship.mjs";
import { executeTurn } from "../../src/game/executeTurn.mjs";
import { createFaction, createShip } from "../../src/setupHelpers.mjs";

describe("executeTurn", () => {
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

	it("moves that are submitted should be executed, and ships without moves should make empty moves", async () => {
		const faction = await createFaction({ name: "Test Faction" });
		const ship1 = await createShip({ faction, location: new Point(0, 0) });
		const ship2 = await createShip({ faction, location: new Point(0, 1) });

		const moves = Map([
			[ship1.id, { token: MovementToken.Forward }],
			[ship2.id + 1, { token: MovementToken.Forward }] // should be ignored
		]);

		await executeTurn(faction.id, moves);

		const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
		const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });

		expect(foundShip1.location).to.deep.equal(new Point(1, 0));
		expect(foundShip1.heading).to.equal(Heading.East);
		expect(foundShip2.location).to.deep.equal(new Point(0, 1));
		expect(foundShip2.heading).to.equal(Heading.East);
	});

	it("a ship shot by two other ships in the same turn should take damage from both", async () => {
		const faction1 = await createFaction({ name: "Test Faction 1" });
		const faction2 = await createFaction({ name: "Test Faction 2" });
		const ship1 = await createShip({ faction: faction1, location: new Point(0, 0) });
		const ship2 = await createShip({ faction: faction2, location: new Point(0, 1) });
		const ship3 = await createShip({ faction: faction2, location: new Point(1, 0), heading: Heading.North });

		const moves = Map([
			[ship2.id, { fire: { left: true } }],
			[ship3.id, { fire: { left: true } }]
		]);

		await executeTurn(faction2.id, moves);

		const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
		expect(foundShip1.damage).to.equal(30); // 15 from each shot
	});

	it("a ship that has damage greater than or equal to its hull at the end of a turn should be marked as sunk", async () => {
		const faction = await createFaction({ name: "Test Faction" });
		const ship = await createShip({ faction, location: new Point(0, 0), damage: 89 });

		const moves = Map([
			[ship.id, { token: MovementToken.Forward }]
		]);

		await executeTurn(faction.id, moves);

		const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
		expect(foundShip.damage).to.equal(90);
		expect(foundShip.sunk).to.be.true;
	});

	it("a ship that has sunk should not be able to move", async () => {
		const faction = await createFaction({ name: "Test Faction" });
		const ship = await createShip({ faction, location: new Point(0, 0), sunk: true });

		const moves = Map([
			[ship.id, { token: MovementToken.Forward }]
		]);

		await executeTurn(faction.id, moves);

		const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
		expect(foundShip.location.x).to.equal(0);
		expect(foundShip.location.y).to.equal(0);
	});

	it("attempting to execute an illegal turn should execute as if no moves were submitted for that turn", async () => {
		const faction = await createFaction({ name: "Test Faction" });
		const ship1 = await createShip({ faction, location: new Point(0, 0), forwardTokens: 0 });
		const ship2 = await createShip({ faction, location: new Point(0, 1) });

		const moves = Map([
			[ship1.id, { token: MovementToken.Forward }],
			[ship2.id, { token: MovementToken.Forward }]
		]);

		await executeTurn(faction.id, moves);

		const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
		const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });

		expect(foundShip1.location.x).to.equal(0);
		expect(foundShip1.location.y).to.equal(0);
		expect(foundShip2.location.x).to.equal(0); // movement cancelled due to illegal move on ship 1
		expect(foundShip2.location.y).to.equal(1);
	});
});

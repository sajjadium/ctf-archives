/* eslint-disable @typescript-eslint/no-unused-vars, max-len */

import { use as chaiUse } from "chai";
import chaiAsPromised from "chai-as-promised";
import { beforeEach,describe, it } from "mocha";

chaiUse(chaiAsPromised);
import { expect } from "chai";

import { Heading, MovementToken, Point, ShipType } from "@puzzled/types";

import { dataSource } from "../../src/dataSource.mjs";
import { Faction } from "../../src/entities/Faction.mjs";
import { Ship } from "../../src/entities/Ship.mjs";
import { executeMove } from "../../src/game/executeMove.mjs";
import {
	createBuoy,
	createFaction,
	createGust,
	createRock,
	createShip,
	createWhirlpool
} from "../../src/setupHelpers.mjs";

describe("executeMove", () => {
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

	describe("movement", () => {
		it("an empty move should leave the ship in place", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, {});
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(0);
		});

		it("a forward move should move the ship forward", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(1);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(1);
		});

		it("a left move should move the ship forward and left, and rotate it left", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction, location: new Point(0, 1) });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Left });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(1);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.North);
			expect(foundShip.damage).to.equal(1);
		});

		it("a right move should move the ship forward and right, and rotate it right", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship,{ token: MovementToken.Right });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(1);
			expect(foundShip.location.y).to.equal(1);
			expect(foundShip.heading).to.equal(Heading.South);
			expect(foundShip.damage).to.equal(1);
		});

		it("attempting a move without a token should throw an error", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction, forwardTokens: 0 });

			await dataSource.transaction(async (tx) => {
				await expect(
					executeMove(tx, ship, { token: MovementToken.Forward})
				).to.eventually.be.rejectedWith(Error);
			});
		});

		it("attempting to move out of bounds should cause the ship to take damage", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction, location: new Point(0, 0), heading: Heading.North });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.North);
			expect(foundShip.damage).to.equal(11);
		});
	});

	describe("ramming", () => {
		it("attempting to move forward into the same tile as a ship from another faction should damage both ships and prevent the movement", async () => {
			const faction1 = await createFaction({ name: "Test Faction 1" });
			const faction2 = await createFaction({ name: "Test Faction 2" });
			const ship1 = await createShip({ faction: faction1 });
			const ship2 = await createShip({ faction: faction2, location: new Point(1, 0), type: ShipType.Galleon });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship1, { token: MovementToken.Forward });
			});

			const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
			expect(foundShip1.location.x).to.equal(0);
			expect(foundShip1.location.y).to.equal(0);
			expect(foundShip1.heading).to.equal(Heading.East);
			expect(foundShip1.damage).to.equal(21);

			const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });
			expect(foundShip2.location.x).to.equal(1);
			expect(foundShip2.location.y).to.equal(0);
			expect(foundShip2.heading).to.equal(Heading.East);
			expect(foundShip2.damage).to.equal(10);
		});

		it("attempting to turn into the same tile as a ship from another faction should damage both ships and prevent the movement but still allow the ship to turn", async () => {
			const faction1 = await createFaction({ name: "Test Faction 1" });
			const faction2 = await createFaction({ name: "Test Faction 2" });
			const ship1 = await createShip({ faction: faction1 });
			const ship2 = await createShip({ faction: faction2, location: new Point(1, 0), type: ShipType.Galleon });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship1, { token: MovementToken.Left });
			});

			const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
			expect(foundShip1.location.x).to.equal(0);
			expect(foundShip1.location.y).to.equal(0);
			expect(foundShip1.heading).to.equal(Heading.North);
			expect(foundShip1.damage).to.equal(21);

			const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });
			expect(foundShip2.location.x).to.equal(1);
			expect(foundShip2.location.y).to.equal(0);
			expect(foundShip2.heading).to.equal(Heading.East);
			expect(foundShip2.damage).to.equal(10);
		});
	});

	describe("rocks", () => {
		it("a rock should damage the ship and prevent the ship from moving forward into it", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createRock(new Point(1, 0));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(11);
		});

		it("a rock should damage the ship and prevent the ship from moving into it but still allow the ship to turn", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createRock(new Point(1, 0));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Right });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.South);
			expect(foundShip.damage).to.equal(11);
		});
	});

	describe("gusts", () => {
		it("a gust should move the ship in the direction of the gust if the ship moves on top of it", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createGust(new Point(1, 0), Heading.East);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(2);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(1);
		});

		it("a gust should move the ship in the direction of the gust if the ship is on top of it and doesn't move", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createGust(new Point(0, 0), Heading.South);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, {});
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(1);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(0);
		});

		it("a ship should only interact with one gust per move", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createGust(new Point(1, 0), Heading.East);
			await createGust(new Point(2, 0), Heading.East);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(2);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(1);
		});

		it("a ship blown into a rock by a gust shouldn't be moved and should take damage", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createGust(new Point(1, 0), Heading.East);
			await createRock(new Point(2, 0));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(1);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(11);
		});

		it("a ship blown into an enemy ship by a gust shouldn't be moved and should take damage", async () => {
			const faction1 = await createFaction({ name: "Test Faction 1" });
			const faction2 = await createFaction({ name: "Test Faction 2" });
			const ship1 = await createShip({ faction: faction1 });
			const ship2 = await createShip({ faction: faction2, location: new Point(2, 0) });
			await createGust(new Point(1, 0), Heading.East);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship1, { token: MovementToken.Forward });
			});

			const foundShip1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship1.id });
			expect(foundShip1.location.x).to.equal(1);
			expect(foundShip1.location.y).to.equal(0);
			expect(foundShip1.heading).to.equal(Heading.East);
			expect(foundShip1.damage).to.equal(11);

			const foundShip2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship2.id });
			expect(foundShip2.location.x).to.equal(2);
			expect(foundShip2.location.y).to.equal(0);
			expect(foundShip2.heading).to.equal(Heading.East);
			expect(foundShip2.damage).to.equal(10);
		});
	});

	describe("whirlpools", () => {
		it("a whirlpool should move and rotate the ship if the ship moves on top of it", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createWhirlpool(new Point(1.5, 0.5), true);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(2);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.South);
			expect(foundShip.damage).to.equal(1);
		});

		it("a whirlpool should move and rotate the ship if the ship is on top of it and doesn't move", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createWhirlpool(new Point(0.5, 0.5), false);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, {});
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(0);
			expect(foundShip.location.y).to.equal(1);
			expect(foundShip.heading).to.equal(Heading.North);
			expect(foundShip.damage).to.equal(0);
		});

		it("a whirlpool should not move a ship if the ship interacted with a gust", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			await createGust(new Point(1, 0), Heading.East);
			await createWhirlpool(new Point(1.5, 0.5), true);

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const foundShip = await dataSource.getRepository(Ship).findOneByOrFail({ id: ship.id });
			expect(foundShip.location.x).to.equal(2);
			expect(foundShip.location.y).to.equal(0);
			expect(foundShip.heading).to.equal(Heading.East);
			expect(foundShip.damage).to.equal(1);
		});
	});

	describe("firing", () => {
		it("firing to the left should hit the nearest ship of another faction to the left", async () => {
			const f1 = await createFaction({ name: "Test Faction 1" });
			const f2 = await createFaction({ name: "Test Faction 2" });
			const s1 = await createShip({ faction: f1, location: new Point(0, 3), heading: Heading.East });
			const s2 = await createShip({ faction: f1, location: new Point(0, 2), heading: Heading.East });
			const s3 = await createShip({ faction: f2, location: new Point(0, 1), heading: Heading.East });
			const s4 = await createShip({ faction: f2, location: new Point(0, 1), heading: Heading.East });
			const s5 = await createShip({ faction: f2, location: new Point(0, 0), heading: Heading.East });
			const s6 = await createShip({ faction: f2, location: new Point(1, 2), heading: Heading.East });
			const s7 = await createShip({ faction: f2, location: new Point(0, 4), heading: Heading.East });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, s1, { fire: { left: true } });
			});

			const foundS1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s1.id });
			const foundS2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s2.id });
			const foundS3 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s3.id });
			const foundS4 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s4.id });
			const foundS5 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s5.id });
			const foundS6 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s6.id });
			const foundS7 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s7.id });

			expect(foundS1.damage).to.equal(0);
			expect(foundS2.damage).to.equal(0);
			expect(foundS3.damage).to.equal(15);
			expect(foundS4.damage).to.equal(0); // ties broken by id
			expect(foundS5.damage).to.equal(0);
			expect(foundS6.damage).to.equal(0);
			expect(foundS7.damage).to.equal(0);
		});

		it("firing to the right should hit the nearest ship of another faction to the right", async () => {
			const f1 = await createFaction({ name: "Test Faction 1" });
			const f2 = await createFaction({ name: "Test Faction 2" });
			const s1 = await createShip({ faction: f1, location: new Point(0, 1), heading: Heading.East });
			const s2 = await createShip({ faction: f1, location: new Point(0, 2), heading: Heading.East });
			const s3 = await createShip({ faction: f2, location: new Point(0, 3), heading: Heading.East });
			const s4 = await createShip({ faction: f2, location: new Point(0, 3), heading: Heading.East });
			const s5 = await createShip({ faction: f2, location: new Point(0, 4), heading: Heading.East });
			const s6 = await createShip({ faction: f2, location: new Point(1, 2), heading: Heading.East });
			const s7 = await createShip({ faction: f2, location: new Point(0, 0), heading: Heading.East });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, s1, { fire: { right: true } });
			});

			const foundS1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s1.id });
			const foundS2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s2.id });
			const foundS3 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s3.id });
			const foundS4 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s4.id });
			const foundS5 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s5.id });
			const foundS6 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s6.id });
			const foundS7 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s7.id });

			expect(foundS1.damage).to.equal(0);
			expect(foundS2.damage).to.equal(0);
			expect(foundS3.damage).to.equal(15);
			expect(foundS4.damage).to.equal(0); // ties broken by id
			expect(foundS5.damage).to.equal(0);
			expect(foundS6.damage).to.equal(0);
			expect(foundS7.damage).to.equal(0);
		});

		it("firing at a ship that is too far away should not hit it", async () => {
			const f1 = await createFaction({ name: "Test Faction 1" });
			const f2 = await createFaction({ name: "Test Faction 2" });
			const s1 = await createShip({ faction: f1, location: new Point(4, 0), heading: Heading.North });
			const s2 = await createShip({ faction: f2, location: new Point(0, 0), heading: Heading.East });

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, s1, { fire: { left: true } });
			});

			const foundS1 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s1.id });
			const foundS2 = await dataSource.getRepository(Ship).findOneByOrFail({ id: s2.id });

			expect(foundS1.damage).to.equal(0);
			expect(foundS2.damage).to.equal(0);
		});

		it("attempting to fire without any loaded cannons should throw an error", async () => {
			const f1 = await createFaction({ name: "Test Faction 1" });
			const f2 = await createFaction({ name: "Test Faction 2" });
			const s1 = await createShip({ faction: f1, location: new Point(1, 0), heading: Heading.North, loadedCannons: 0 });
			const s2 = await createShip({ faction: f2, location: new Point(0, 0), heading: Heading.East });

			await expect(
				dataSource.transaction(async (tx) => {
					await executeMove(tx, s1, { fire: { left: true } });
				}),
			).to.eventually.be.rejectedWith(Error);
		});
	});

	describe("buoys", () => {
		it("a ship should score 1 point for a buoy if it starts and ends in its influence zone", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			const buoy = await createBuoy(new Point(1, 0));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, {});
			});

			const updatedFaction = await dataSource.getRepository(Faction).findOneByOrFail({ id: faction.id });
			expect(updatedFaction.score).to.equal(1);
		});

		it("a ship should score 2 points for a buoy if it moves into its influence zone", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction });
			const buoy = await createBuoy(new Point(2, 0));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const updatedFaction = await dataSource.getRepository(Faction).findOneByOrFail({ id: faction.id });
			expect(updatedFaction.score).to.equal(2);
		});

		it("a ship should be able to score on multiple buoys in the same turn", async () => {
			const faction = await createFaction({ name: "Test Faction" });
			const ship = await createShip({ faction, location: Point.Origin, heading: Heading.South });
			const buoy1 = await createBuoy(new Point(1, 0));
			const buoy2 = await createBuoy(new Point(1, 2));

			await dataSource.transaction(async (tx) => {
				await executeMove(tx, ship, { token: MovementToken.Forward });
			});

			const updatedFaction = await dataSource.getRepository(Faction).findOneByOrFail({ id: faction.id });
			expect(updatedFaction.score).to.equal(3);
		});
	});
});
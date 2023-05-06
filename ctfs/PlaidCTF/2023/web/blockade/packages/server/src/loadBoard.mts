import { BoardInfo } from "@puzzled/types";

import { createBuoy, createGust, createRock, createWhirlpool } from "./setupHelpers.mjs";

export async function loadBoard(info: BoardInfo) {
	for (const rock of info.rocks) {
		await createRock(rock.location);
	}

	for (const gust of info.gusts) {
		await createGust(gust.location, gust.heading);
	}

	for (const whirlpool of info.whirlpools) {
		await createWhirlpool(whirlpool.location, whirlpool.clockwise);
	}

	for (const buoy of info.buoys) {
		await createBuoy(buoy.location, buoy.value);
	}
}

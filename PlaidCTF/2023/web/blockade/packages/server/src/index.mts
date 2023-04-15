import { Mutex } from "async-mutex";
import { Map } from "immutable";
import { Server } from "socket.io";
import { z } from "zod";

import { ClientEvents, ServerEvents } from "@puzzled/messages";
import { FactionRoundMoves, GameState, Move, RoundOutcome } from "@puzzled/types";

import { AI } from "./ai/index.mjs";
import { Board } from "./data/board.mjs";
import { createAiShips, createPlayerShips } from "./data/ships.mjs";
import { dataSource } from "./dataSource.mjs";
import { Faction } from "./entities/Faction.mjs";
import { executeRound } from "./game/executeRound.mjs";
import { getState } from "./getState.mjs";
import { loadBoard } from "./loadBoard.mjs";
import { createFaction } from "./setupHelpers.mjs";

// TODO(bluepichu): decide if I want to keep the time limit...
// const RoundTime = 35000;
const RoundTime = 1000000000;
const MaxRounds = 75;
const RoundMutex = new Mutex();
const Flag = process.env["FLAG"] ?? "PCTF{test_flag}";

async function main() {
	await dataSource.initialize();
	await dataSource.dropDatabase();
	await dataSource.synchronize();

	await loadBoard(Board);
	const playerFaction = await createFaction({ name: "Player Faction" });
	const aiFaction = await createFaction({ name: "AI Faction", score: 3500 }); // they have a bit of a lead...
	await createPlayerShips(playerFaction);
	await createAiShips(aiFaction);

	const ai = new AI(aiFaction);
	const io = new Server<ClientEvents, ServerEvents>();

	let round = 35; // oops, we showed up late...
	let roundTimeout: NodeJS.Timeout | undefined;
	let started = false;
	let won = false;
	let nextPlayerMoves: FactionRoundMoves = Map();

	async function advanceRound(toRound: number) {
		await RoundMutex.runExclusive(async () => {
			if (round >= MaxRounds) {
				return;
			}

			if (toRound !== round + 1) {
				return;
			}

			if (roundTimeout !== undefined) {
				clearTimeout(roundTimeout);
			}

			round++;

			const roundOutcome = await executeRound(
				Map([
					[playerFaction.id, nextPlayerMoves],
					[aiFaction.id, ai.getMoves(await getState(round, aiFaction.id))]
				]),
				round % 2 === 0 ? [playerFaction.id, aiFaction.id] : [aiFaction.id, playerFaction.id]
			);

			io.to("player").emit("round", RoundOutcome.toJson(roundOutcome));
			io.to("player").emit("state", GameState.toJson(await getState(round, playerFaction.id)));
			nextPlayerMoves = Map();

			if (round >= MaxRounds) {
				const updatedPlayerFaction = await (
					dataSource.getRepository(Faction)
						.findOneByOrFail({ id: playerFaction.id })
				);

				const updatedAiFaction = await (
					dataSource.getRepository(Faction)
						.findOneByOrFail({ id: aiFaction.id })
				);

				if (updatedPlayerFaction.score > updatedAiFaction.score) {
					won = true;
					io.to("player").emit("flag", Flag);
				}
			} else {
				roundTimeout = setTimeout(() => advanceRound(round + 1), RoundTime);
			}
		});
	}

	io.on("connection", async (socket) => {
		socket.join("player");

		if (won) {
			socket.emit("flag", Flag);
		}

		socket.on("start", () => {
			if (started) {
				return;
			}

			started = true;

			roundTimeout = setTimeout(() => advanceRound(1), RoundTime);
		});

		const SetMovesArgsSchema = z.object({
			id: z.number(),
			moves: z.tuple([
				Move.Schema,
				Move.Schema,
				Move.Schema,
				Move.Schema,
			])
		});

		socket.on("setMoves", (args: unknown) => {
			const { id, moves } = SetMovesArgsSchema.parse(args);
			nextPlayerMoves = nextPlayerMoves.set(id, moves);
			socket.broadcast.to("player").emit("movesUpdated", { id, moves });
		});

		const AdvanceRoundArgsSchema = z.object({
			round: z.number()
		});

		socket.on("advanceRound", (args: unknown) => {
			const { round: clientRound } = AdvanceRoundArgsSchema.parse(args);
			advanceRound(clientRound);
		});

		socket.emit("board", Board);
		socket.emit("state", GameState.toJson(await getState(round, playerFaction.id)));

		nextPlayerMoves.forEach((moves, id) => {
			socket.emit("movesUpdated", { id, moves });
		});
	});

	io.listen(2008);
}

main();

import { z, ZodSchema } from "zod";
import { MovementToken } from "./MovementToken.mjs";

export interface Move {
	token?: MovementToken;
	fire?: {
		left?: boolean;
		right?: boolean;
	};
}

export namespace Move {
	export const Schema: ZodSchema<Move> = z.object({
		token: z.optional(z.nativeEnum(MovementToken)),
		fire: z.optional(
			z.object({
				left: z.optional(z.boolean()),
				right: z.optional(z.boolean()),
			}),
		),
	});

	export function empty(): Move {
		return {};
	}

	export function clone(move: Move): Move {
		return {
			token: move.token,
			fire: move.fire ? { left: move.fire.left, right: move.fire.right } : undefined,
		};
	}
}

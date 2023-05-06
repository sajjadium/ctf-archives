import { createPool, createSqlTag } from "slonik";

import { EpisodeSchema, GenreSchema, PlaylistSchema, ShowSchema, UserSchema } from "./types.mjs";

export const pool = await createPool(process.env.PG_URL ?? "postgres://postgres");

export const sql = createSqlTag({
	typeAliases: {
		Show: ShowSchema,
		Episode: EpisodeSchema,
		Genre: GenreSchema,
		Playlist: PlaylistSchema,
		User: UserSchema
	}
});

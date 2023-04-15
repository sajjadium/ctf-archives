import { z } from "zod";

export const ShowSchema = z.object({
	id: z.string(),
	name: z.string(),
	coverUrl: z.string(),
	description: z.string(),
	owner: z.string(),
});

export type Show = z.infer<typeof ShowSchema>;

export const EpisodeSchema = z.object({
	id: z.string(),
	name: z.string(),
	description: z.string(),
	url: z.string(),
	createdAt: z.string(),
	show: z.string(),
	rating: z.number(),
	ratingCount: z.number(),
});

export type Episode = z.infer<typeof EpisodeSchema>;

export const GenreSchema = z.object({
	id: z.string(),
	name: z.string(),
});

export type Genre = z.infer<typeof GenreSchema>;

export const PlaylistSchema = z.object({
	id: z.string(),
	name: z.string(),
	owner: z.string(),
	description: z.string(),
	episodes: z.array(z.string()),
});

export type Playlist = z.infer<typeof PlaylistSchema>;

export const UserSchema = z.object({
	id: z.string(),
	name: z.string(),
});

export type User = z.infer<typeof UserSchema>;

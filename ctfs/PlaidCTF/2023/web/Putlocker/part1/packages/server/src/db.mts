import { compare, hash } from "bcrypt";
import { NotFoundError } from "slonik";
import { z } from "zod";

import { pool, sql } from "./sql.mjs";
import { Episode, Genre, Playlist, Show, User } from "./types.mjs";

const showSelect = sql.typeAlias("Show")`
	id,
	name,
	cover_url AS "coverUrl",
	description,
	owner
`;

export function loadShow(id: string): Promise<Show> {
	return pool.one(sql.typeAlias("Show")`
		SELECT ${showSelect}
		FROM shows
		WHERE shows.id = ${id}
	`);
}

export function loadAllShows(): Promise<readonly Show[]> {
	return pool.any(sql.typeAlias("Show")`
		SELECT ${showSelect}
		FROM shows
	`);
}

export function loadUserShows(userId: string): Promise<readonly Show[]> {
	return pool.any(sql.typeAlias("Show")`
		SELECT ${showSelect}
		FROM shows
		WHERE shows.owner = ${userId}
	`);
}

const episodeSelect = sql.typeAlias("Episode")`
	episodes.id,
	episodes.name,
	episodes.description,
	episodes.url,
	episodes.created_at AS "createdAt",
	episodes.show,
	avg(user_episode_ratings.rating) AS rating,
	count(user_episode_ratings.rating) AS "ratingCount"
`;

export function loadEpisode(id: string): Promise<Episode> {
	return pool.one(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		WHERE episodes.id = ${id}
		GROUP BY episodes.id
	`);
}

export function loadRecentEpisodes(): Promise<readonly Episode[]> {
	return pool.any(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		GROUP BY episodes.id
		ORDER BY episodes.created_at DESC
		LIMIT 16
	`);
}

export function loadShowEpisodes(id: string): Promise<readonly Episode[]> {
	return pool.any(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		WHERE episodes.show = ${id}
		GROUP BY episodes.id
		ORDER BY episodes.index
	`);
}

export function loadPlaylistEpisodes(id: string): Promise<readonly Episode[]> {
	return pool.any(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes
			LEFT JOIN playlist_episodes ON playlist_episodes.episode = episodes.id
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		WHERE playlist_episodes.playlist = ${id}
		GROUP BY episodes.id, playlist_episodes.index
		ORDER BY playlist_episodes.index
	`);
}

export function loadPreviousEpisode(id: string): Promise<Episode | null> {
	return pool.maybeOne(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes current_episode
			LEFT JOIN episodes ON episodes.show = current_episode.show AND episodes.index = current_episode.index - 1
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		WHERE current_episode.id = ${id}
		GROUP BY episodes.id
	`);
}

export function loadNextEpisode(id: string): Promise<Episode | null> {
	return pool.maybeOne(sql.typeAlias("Episode")`
		SELECT ${episodeSelect}
		FROM episodes current_episode
			LEFT JOIN episodes ON episodes.show = current_episode.show AND episodes.index = current_episode.index + 1
			LEFT JOIN user_episode_ratings ON user_episode_ratings.episode = episodes.id
		WHERE current_episode.id = ${id}
		GROUP BY episodes.id
	`);
}

export function loadGenre(id: string): Promise<Genre> {
	return pool.one(sql.typeAlias("Genre")`
		SELECT
			id,
			name
		FROM genres
		WHERE genres.id = ${id}
	`);
}

export function loadAllGenres(): Promise<readonly Genre[]> {
	return pool.any(sql.typeAlias("Genre")`
		SELECT
			id,
			name
		FROM genres
	`);
}

export function loadShowGenres(id: string): Promise<readonly Genre[]> {
	return pool.any(sql.typeAlias("Genre")`
		SELECT
			id,
			name
		FROM genres
			LEFT JOIN show_genres ON show_genres.genre = genres.id
		WHERE show_genres.show = ${id}
	`);
}

export function loadGenreShows(id: string): Promise<readonly Show[]> {
	return pool.any(sql.typeAlias("Show")`
		SELECT
			id,
			name,
			description
		FROM shows
			LEFT JOIN show_genres ON show_genres.show = shows.id
		WHERE show_genres.genre = ${id}
	`);
}

const playlistSelect = sql.typeAlias("Playlist")`
	id,
	name,
	owner,
	description,
	array_agg(playlist_episodes.episode) AS episodes
`;

export function loadPlaylist(id: string): Promise<Playlist> {
	return pool.one(sql.typeAlias("Playlist")`
		SELECT ${playlistSelect}
		FROM playlists
			LEFT JOIN playlist_episodes ON playlist_episodes.playlist = playlists.id
		WHERE playlists.id = ${id}
		GROUP BY playlists.id
	`);
}

export function loadUserPlaylists(id: string): Promise<readonly Playlist[]> {
	return pool.any(sql.typeAlias("Playlist")`
		SELECT ${playlistSelect}
		FROM playlists
			LEFT JOIN playlist_episodes ON playlist_episodes.playlist = playlists.id
		WHERE playlists.owner = ${id}
		GROUP BY playlists.id
	`);
}

export function loadUser(id: string): Promise<User> {
	return pool.one(sql.typeAlias("User")`
		SELECT
			id,
			name
		FROM users
		WHERE users.id = ${id}
	`);
}

export async function createUser(name: string, password: string): Promise<string> {
	return await pool.transaction(async (tx) => {
		const passwordHash = await hash(password, 12);

		const result = await tx.one(sql.type(z.object({ id: z.string() }))`
			INSERT INTO users (name, password)
			VALUES (${name}, ${passwordHash})
			RETURNING id
		`);

		return result.id;
	});
}

export async function setAdminPassword(password: string): Promise<void> {
	const passwordHash = await hash(password, 12);

	await pool.query(sql.unsafe`
		UPDATE users
		SET password = ${passwordHash}
		WHERE name = 'admin'
	`);
}

export async function login(name: string, password: string): Promise<string | null> {
	const result = await pool.one(sql.type(z.object({ id: z.string(), password: z.string() }))`
		SELECT id, password
		FROM users
		WHERE name = ${name}
	`);

	if (await compare(password, result.password)) {
		return result.id;
	}

	return null;
}

export async function createShow(
	name: string,
	description: string,
	coverUrl: string,
	genres: readonly string[],
	userId: string
): Promise<string> {
	return await pool.transaction(async (tx) => {
		const result = await tx.one(sql.type(z.object({ id: z.string() }))`
			INSERT INTO shows (name, description, cover_url, owner)
			VALUES (${name}, ${description}, ${coverUrl}, ${userId})
			RETURNING id
		`);

		const showId = result.id;

		await tx.any(sql.type(z.object({}))`
			INSERT INTO show_genres (show, genre)
			SELECT ${showId}, id
			FROM genres
			WHERE id = ANY(${sql.array(genres, "uuid")})
		`);

		return showId;
	});
}

export async function updateShow(
	id: string,
	name: string,
	description: string,
	coverUrl: string,
	genres: readonly string[],
	userId: string
): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			UPDATE shows
			SET
				name = ${name},
				description = ${description},
				cover_url = ${coverUrl}
			WHERE id = ${id} AND owner = ${userId}
			RETURNING id
		`);

		await tx.any(sql.type(z.object({}))`
			DELETE FROM show_genres
			WHERE show = ${id}
		`);

		await tx.any(sql.type(z.object({}))`
			INSERT INTO show_genres (show, genre)
			SELECT ${id}, id
			FROM genres
			WHERE id = ANY(${sql.array(genres, "uuid")})
		`);
	});
}

export async function createEpisode(
	showId: string,
	name: string,
	description: string,
	url: string,
	userId: string
): Promise<string> {
	return await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			SELECT id
			FROM shows
			WHERE id = ${showId} AND owner = ${userId}
		`);

		const indexResult = await tx.one(sql.type(z.object({ index: z.number() }))`
			SELECT COALESCE(MAX(index), -1) + 1 AS index
			FROM episodes
			WHERE show = ${showId}
		`);

		const result = await tx.one(sql.type(z.object({ id: z.string() }))`
			INSERT INTO episodes (show, index, name, description, url)
			VALUES (${showId}, ${indexResult.index}, ${name}, ${description}, ${url})
			RETURNING id
		`);

		return result.id;
	});
}

export async function updateEpisode(
	id: string,
	name: string,
	description: string,
	url: string,
	userId: string
): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			UPDATE episodes
			SET
				name = ${name},
				description = ${description},
				url = ${url}
			WHERE id = ${id} AND show IN (
				SELECT id
				FROM shows
				WHERE owner = ${userId}
			)
			RETURNING id
		`);
	});
}

export async function deleteEpisode(id: string, userId: string): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			DELETE FROM episodes
			WHERE id = ${id} AND show IN (
				SELECT id
				FROM shows
				WHERE owner = ${userId}
			)
			RETURNING id
		`);
	});
}

export async function createPlaylist(
	name: string,
	description: string,
	userId: string
): Promise<string> {
	return await pool.transaction(async (tx) => {
		const result = await tx.one(sql.type(z.object({ id: z.string() }))`
			INSERT INTO playlists (owner, name, description)
			VALUES (${userId}, ${name}, ${description})
			RETURNING id
		`);

		return result.id;
	});
}

export async function updatePlaylist(
	id: string,
	name: string,
	description: string,
	userId: string
): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			UPDATE playlists
			SET name = ${name}, description = ${description}
			WHERE id = ${id} AND owner = ${userId}
			RETURNING id
		`);
	});
}

export async function updatePlaylistEpisodes(
	id: string,
	episodes: readonly string[],
	userId: string
): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			SELECT id
			FROM playlists
			WHERE id = ${id} AND owner = ${userId}
		`);

		await tx.any(sql.type(z.object({ id: z.string() }))`
			DELETE FROM playlist_episodes
			WHERE playlist = ${id}
		`);

		await tx.any(sql.type(z.object({}))`
			INSERT INTO playlist_episodes (playlist, episode, index)
			SELECT *
			FROM ${sql.unnest(
				episodes.map((episode, index) => [id, episode, index]),
				["uuid", "uuid", "int4"]
			)} to_insert (playlist, episode, index)
		`);
	});
}

export async function deletePlaylist(id: string, userId: string): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.one(sql.type(z.object({ id: z.string() }))`
			SELECT id
			FROM playlists
			WHERE id = ${id} AND owner = ${userId}
		`);

		await tx.any(sql.type(z.object({}))`
			DELETE FROM playlist_episodes
			WHERE playlist = ${id}
		`);

		await tx.one(sql.type(z.object({ id: z.string() }))`
			DELETE FROM playlists
			WHERE id = ${id} AND owner = ${userId}
			RETURNING id
		`);
	});
}

export async function rateEpisode(
	episodeId: string,
	rating: number,
	userId: string
): Promise<void> {
	await pool.transaction(async (tx) => {
		await tx.any(sql.type(z.object({}))`
			INSERT INTO user_episode_ratings (episode, rating, "user")
			VALUES (${episodeId}, ${rating}, ${userId})
			ON CONFLICT (episode, "user") DO UPDATE SET rating = ${rating}
		`);
	});
}

export async function notFoundToNull<T>(promise: Promise<T>): Promise<T | null> {
	try {
		return await promise;
	} catch (error) {
		if (error instanceof NotFoundError) {
			return null;
		}

		throw error;
	}
}

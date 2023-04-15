import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

import { assertAdmin, assertLoggedIn } from "./auth.mjs";
import { Context } from "./context.mjs";
import {
	createEpisode,
	createPlaylist,
	createShow,
	createUser,
	deleteEpisode,
	deletePlaylist,
	loadAllGenres,
	loadAllShows,
	loadEpisode,
	loadGenre,
	loadGenreShows,
	loadNextEpisode,
	loadPlaylist,
	loadPlaylistEpisodes,
	loadPreviousEpisode,
	loadRecentEpisodes,
	loadShow,
	loadShowEpisodes,
	loadShowGenres,
	loadUser,
	loadUserPlaylists,
	loadUserShows,
	login,
	notFoundToNull,
	rateEpisode,
	setAdminPassword,
	updateEpisode,
	updatePlaylist,
	updatePlaylistEpisodes,
	updateShow
} from "./db.mjs";
import { generateUserToken, verifyUserToken } from "./jwt.mjs";
import { renderHtml } from "./renderHtml.mjs";
import { checkUrl } from "./report.mjs";
import { pool } from "./sql.mjs";
import { Episode, Genre, Playlist, Show, User } from "./types.mjs";

const Flag = process.env["FLAG"] ?? "PCTF{fake_flag}";



const typeDefs = `
	type Show {
		id: ID!
		name: String!
		description: String!
		rawDescription: String!
		coverUrl: String!
		genres: [Genre!]!
		episodes: [Episode!]!
		owner: User!
	}

	type Episode {
		id: ID!
		name: String!
		url: String!
		createdAt: String!
		description: String!
		rawDescription: String!
		show: Show!
		rating: Float
		ratingCount: Int!
		previous: Episode
		next: Episode
	}

	type Genre {
		id: ID!
		name: String!
		shows: [Show!]!
	}

	type Playlist {
		id: ID!
		name: String!
		owner: User!
		description: String!
		episodes: [Episode!]!
		episodeCount: Int!
	}

	type User {
		id: ID!
		name: String!
		shows: [Show!]!
		playlists: [Playlist!]!
	}

	type Query {
		show(id: ID!): Show
		episode(id: ID!): Episode
		genre(id: ID!): Genre
		playlist(id: ID!): Playlist
		user(id: ID!): User

		allShows: [Show!]!
		allGenres: [Genre!]!

		featuredShow: Show
		recentEpisodes: [Episode!]!

		self: User
	}

	type Mutation {
		register(name: String!, password: String!): String
		login(name: String!, password: String!): String

		createShow(name: String!, description: String!, coverUrl: String!, genres: [ID!]!): Show
		updateShow(id: ID!, name: String!, description: String!, coverUrl: String!, genres: [ID!]!): Show

		createEpisode(show: ID!, name: String!, description: String!, url: String!): Episode
		updateEpisode(id: ID!, name: String!, description: String!, url: String!): Episode
		deleteEpisode(id: ID!): Boolean

		createPlaylist(name: String!, description: String!): Playlist
		updatePlaylist(id: ID!, name: String!, description: String!): Playlist
		updatePlaylistEpisodes(id: ID!, episodes: [ID!]!): Playlist
		deletePlaylist(id: ID!): Boolean

		rateEpisode(id: ID!, rating: Int!): Boolean

		report(url: String!): Boolean

		flag: String
	}
`;

const resolvers = {
	Show: {
		description: (show: Show) => renderHtml(show.description),
		rawDescription: (show: Show) => show.description,
		genres: (show: Show) => loadShowGenres(show.id),
		episodes: (show: Show) => loadShowEpisodes(show.id),
		owner: (show: Show) => loadUser(show.owner)
	},
	Episode: {
		description: (episode: Episode) => renderHtml(episode.description),
		rawDescription: (episode: Episode) => episode.description,
		show: (episode: Episode) => loadShow(episode.show),
		previous: async (episode: Episode) => notFoundToNull(loadPreviousEpisode(episode.id)),
		next: async (episode: Episode) => notFoundToNull(loadNextEpisode(episode.id))
	},
	Genre: {
		shows: (genre: Genre) => loadGenreShows(genre.id)
	},
	Playlist: {
		owner: (playlist: Playlist) => loadUser(playlist.owner),
		episodes: (playlist: Playlist) => loadPlaylistEpisodes(playlist.id),
		episodeCount: (playlist: Playlist) => loadPlaylistEpisodes(playlist.id).then((episodes) => episodes.length)
	},
	User: {
		shows: (user: User) => loadUserShows(user.id),
		playlists: (user: User) => loadUserPlaylists(user.id)
	},
	Query: {
		show: (_: {}, args: { id: string }) => notFoundToNull(loadShow(args.id)),
		episode: (_: {}, args: { id: string }) => notFoundToNull(loadEpisode(args.id)),
		genre: (_: {}, args: { id: string }) => notFoundToNull(loadGenre(args.id)),
		playlist: (_: {}, args: { id: string }) => notFoundToNull(loadPlaylist(args.id)),
		user: (_: {}, args: { id: string }) => notFoundToNull(loadUser(args.id)),

		allShows: () => loadAllShows(),
		allGenres: () => loadAllGenres(),

		featuredShow: () => loadShow("162f015d-b1ff-47b6-b26b-1c1471f9f7c6"),
		recentEpisodes: () => loadRecentEpisodes(),

		self: async (_: {}, __: {}, context: Context) => {
			if (context.user === undefined) {
				return null;
			}

			return loadUser(context.user);
		}
	},
	Mutation: {
		register: async (_: {}, args: { name: string, password: string }) => {
			if (args.name.length === 0 || args.password.length === 0) {
				throw new Error("Invalid name or password");
			}

			const id = await createUser(args.name, args.password);
			return generateUserToken(id);
		},

		login: async (_: {}, args: { name: string, password: string }) => {
			const userId = await login(args.name, args.password);

			if (userId === null) {
				throw new Error("Invalid name or password");
			}

			return generateUserToken(userId);
		},

		createShow: async (
			_: {},
			args: { name: string, description: string, coverUrl: string, genres: string[] },
			context: Context
		) => {
			assertLoggedIn(context);

			const id = await createShow(args.name, args.description, args.coverUrl, args.genres, context.user);
			return await loadShow(id);
		},

		updateShow: async (
			_: {},
			args: { id: string, name: string, description: string, coverUrl: string, genres: string[] },
			context: Context
		) => {
			assertLoggedIn(context);

			await updateShow(args.id, args.name, args.description, args.coverUrl, args.genres, context.user);
			return await loadShow(args.id);
		},

		createEpisode: async (
			_: {},
			args: { show: string, name: string, description: string, url: string },
			context: Context
		) => {
			assertLoggedIn(context);

			const id = await createEpisode(args.show, args.name, args.description, args.url, context.user);
			return await loadEpisode(id);
		},

		updateEpisode: async (
			_: {},
			args: { id: string, name: string, description: string, url: string },
			context: Context
		) => {
			assertLoggedIn(context);

			await updateEpisode(args.id, args.name, args.description, args.url, context.user);
			return loadEpisode(args.id);
		},

		deleteEpisode: async (
			_: {},
			args: { id: string },
			context: Context
		) => {
			assertLoggedIn(context);

			await deleteEpisode(args.id, context.user);
			return true;
		},

		createPlaylist: async (
			_: {},
			args: { name: string, description: string },
			context: Context
		) => {
			assertLoggedIn(context);

			const id = await createPlaylist(args.name, args.description, context.user);
			return await loadPlaylist(id);
		},

		updatePlaylist: async (
			_: {},
			args: { id: string, name: string, description: string },
			context: Context
		) => {
			assertLoggedIn(context);

			await updatePlaylist(args.id, args.name, args.description, context.user);
			return await loadPlaylist(args.id);
		},

		updatePlaylistEpisodes: async (
			_: {},
			args: { id: string, episodes: string[] },
			context: Context
		) => {
			assertLoggedIn(context);

			await updatePlaylistEpisodes(args.id, args.episodes, context.user);
			return loadPlaylist(args.id);
		},

		deletePlaylist: async (
			_: {},
			args: { id: string },
			context: Context
		) => {
			assertLoggedIn(context);

			await deletePlaylist(args.id, context.user);
			return true;
		},

		rateEpisode: async (
			_: {},
			args: { id: string, rating: number },
			context: Context
		) => {
			assertLoggedIn(context);

			await rateEpisode(args.id, args.rating, context.user);
			return true;
		},

		report: async (_: {}, args: { url: string }) => {
			await checkUrl(args.url);
			return true;
		},

		flag: async (
			_: {},
			args: {},
			context: Context
		) => {
			assertLoggedIn(context);
			await assertAdmin(context);

			return Flag;
		}
	}
};

await setAdminPassword(process.env.ADMIN_PASSWORD ?? "password");

const server = new ApolloServer({
	typeDefs,
	resolvers,
	rootValue: {}
});

startStandaloneServer(server, {
	listen: {
		port: 80
	},
	// eslint-disable-next-line @typescript-eslint/require-await
	context: async ({ req }): Promise<Context> => {
		const token = req.headers.authorization;

		if (token === undefined) {
			return {};
		}

		try {
			const user = verifyUserToken(token);
			return { user };
		} catch (e) {
			return {};
		}
	}
});

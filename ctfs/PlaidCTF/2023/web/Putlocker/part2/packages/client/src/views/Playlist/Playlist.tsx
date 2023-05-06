import { useMutation, useQuery } from "@apollo/client";
import React from "react";
import { Navigate, useNavigate, useParams } from "react-router";
import { Link } from "react-router-dom";

import { client } from "@/apollo";
import { EpisodePanel } from "@/components/EpisodePanel";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { encodeQs, useQs } from "@/utils/qs";
import { uuidify } from "@/utils/uuid";

import { BaseView } from "../BaseView";

import styles from "./Playlist.module.scss";

export const Playlist = () => {
	const params = useParams();
	const id = params.id as string;
	const qs = useQs() as { index?: number, autoplay?: boolean };
	const navigate = useNavigate();

	let redirect = false;

	if (qs.index === undefined || typeof qs.index !== "number") {
		qs.index = 0;
		redirect = true;
	}

	if (qs.autoplay === undefined || typeof qs.autoplay !== "boolean") {
		qs.autoplay = true;
		redirect = true;
	}

	if (redirect) {
		return (
			<Navigate to={`/playlist/${id}?${encodeQs(qs)}`} replace />
		);
	}

	return (
		<PlaylistView
			id={uuidify(id)}
			{...qs}
			onSetIndex={(index: number) => {
				navigate(`/playlist/${id}?${encodeQs({ ...qs, index })}`, { replace: true });
			}}
			onSetAutoplay={(autoplay: boolean) => {
				navigate(`/playlist/${id}?${encodeQs({ ...qs, autoplay })}`, { replace: true });
			}}
		/>
	);
};

interface PlaylistViewProps {
	id: string;
	index?: number;
	autoplay?: boolean;
	onSetIndex: (index: number) => void;
	onSetAutoplay: (autoplay: boolean) => void;
}

const PlaylistView = (props: PlaylistViewProps) => {
	const navigate = useNavigate();

	interface PlaylistQueryResult {
		playlist: {
			id: string;
			name: string;
			description: string;
			episodes: {
				id: string;
				name: string;
			}[];
			owner: {
				id: string;
				name: string;
			};
		};
	}

	const { data, loading, error } = useQuery<PlaylistQueryResult>(gql`
		query PlaylistQuery {
			playlist(id: ${props.id}) {
				id
				name
				description
				episodes {
					id
					name
				}
				owner {
					id
					name
				}
			}
		}
	`);

	interface SelfResult {
		self: {
			id: string;
		} | null;
	}

	const { data: selfData } = useQuery<SelfResult>(gql`
		query SelfQuery {
			self {
				id
			}
		}
	`);

	const [updateEpisodes] = useMutation(gql`
		mutation UpdateEpisodes($id: ID!, $episodes: [ID!]!) {
			updatePlaylistEpisodes(
				id: $id,
				episodes: $episodes
			) {
				id
			}
		}
	`);

	const [deletePlaylist] = useMutation(gql`
		mutation DeletePlaylist {
			deletePlaylist(id: ${props.id})
		}
	`);


	if (loading || error || !data) {
		return null;
	}

	const isOwner = selfData?.self?.id === data.playlist.owner.id;

	const listTop = (
		<>
			<div className={styles.creator}>
				{"Created by "}
				<Link className={styles.link} to={`/user/${data.playlist.owner.id}`}>
					{data.playlist.owner.name}
				</Link>
			</div>
			<div className={styles.controls}>
				<div className={styles.autoplay}>
					<input
						type="checkbox"
						className={styles.checkbox}
						checked={props.autoplay}
						onChange={(e) => props.onSetAutoplay(e.target.checked)}
					/>
					Autoplay
				</div>
				{
					isOwner
						? (
							<div
								className={styles.delete}
								onClick={async () => {
									if (window.confirm("Are you sure you want to delete this playlist?")) {
										await deletePlaylist();
										navigate("/");
										await client.resetStore();
									}
								}}
							>
								Delete Playlist
							</div>
						)
						: null
				}
			</div>
		</>
	);

	if (data.playlist.episodes.length === 0) {
		return (
			<BaseView>
				<div className={classes(styles.playlist, styles.empty)}>
					<Panel
						className={styles.episode}
						title="No Episodes"
					>
						This playlist is empty.  If you are the playlist owner, you can add episodes to it by clicking
						the "Add to Playlist" button on an episode page.
					</Panel>
					<Panel
						className={styles.list}
						title={data.playlist.name}
					>
						{listTop}
						No episodes to show.
					</Panel>
				</div>
			</BaseView>
		);
	}

	let index = props.index ?? 0;

	if (index < 0 || index >= data.playlist.episodes.length) {
		index = 0;
	}

	return (
		<BaseView>
			<div className={styles.playlist}>
				<EpisodePanel
					className={styles.episode}
					id={data.playlist.episodes[index].id}
					autoplay={props.autoplay}
					onComplete={() => {
						if (props.autoplay && index + 1 < data.playlist.episodes.length) {
							props.onSetIndex(index + 1);
						}
					}}
				/>
				<Panel
					className={styles.list}
					title={data.playlist.name}
				>
					{listTop}
					<ul className={styles.episodeList}>
						{
							data.playlist.episodes.map((episode, i) => (
								<li
									key={i}
									className={classes(
										styles.episode,
										i === index ? styles.current : undefined,
										isOwner ? styles.owner : undefined,
									)}
								>
									<div
										className={styles.name}
										onClick={() => props.onSetIndex(i)}
									>
										{episode.name}
									</div>
									{
										isOwner && i > 0
											? (
												<div
													className={styles.moveUp}
													onClick={async () => {
														const newEpisodeIds = [
															...data.playlist.episodes
																.slice(0, i - 1)
																.map((episode) => episode.id),
															data.playlist.episodes[i].id,
															data.playlist.episodes[i - 1].id,
															...data.playlist.episodes
																.slice(i + 1)
																.map((episode) => episode.id)
														];

														await updateEpisodes({
															variables: {
																id: data.playlist.id,
																episodes: newEpisodeIds,
															},
														});
														await client.resetStore();
													}}
												>
													⬆️
												</div>
											)
											: null
									}
									{
										isOwner && i < data.playlist.episodes.length - 1
											? (
												<div
													className={styles.moveDown}
													onClick={async () => {
														const newEpisodeIds = [
															...data.playlist.episodes
																.slice(0, i)
																.map((episode) => episode.id),
															data.playlist.episodes[i + 1].id,
															data.playlist.episodes[i].id,
															...data.playlist.episodes
																.slice(i + 2)
																.map((episode) => episode.id)
														];

														await updateEpisodes({
															variables: {
																id: data.playlist.id,
																episodes: newEpisodeIds,
															},
														});
														await client.resetStore();
													}}
												>
													⬇️
												</div>
											)
											: null
									}
									{
										isOwner
											? (
												<div
													className={styles.remove}
													onClick={async () => {
														const newEpisodeIds = [
															...data.playlist.episodes
																.slice(0, i)
																.map((episode) => episode.id),
															...data.playlist.episodes
																.slice(i + 1)
																.map((episode) => episode.id)
														];

														await updateEpisodes({
															variables: {
																id: data.playlist.id,
																episodes: newEpisodeIds,
															},
														});
														await client.resetStore();
													}}
												>
													❌
												</div>
											)
											: null
									}
								</li>
							))
						}
					</ul>
				</Panel>
			</div>
		</BaseView>
	);
};

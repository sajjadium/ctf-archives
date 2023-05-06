import { useMutation, useQuery } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { client } from "@/apollo";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./AddToPlaylistButton.module.scss";

interface Props {
	className?: string;
	episode: string;
}

export const AddToPlaylistButton = (props: Props) => {
	const navigate = useNavigate();
	const [open, setOpen] = React.useState(false);

	interface SelfPlaylistsResult {
		self: {
			playlists: {
				id: string;
				name: string;
				episodes: {
					id: string;
				}[];
			}[];
		};
	}

	const { data } = useQuery<SelfPlaylistsResult>(gql`
		query SelfPlaylistsQuery {
			self {
				playlists {
					id
					name
					episodes {
						id
					}
				}
			}
		}
	`);

	const [addToPlaylist] = useMutation(gql`
		mutation AddToPlaylist($playlist: ID!, $episodes: [ID!]!) {
			updatePlaylistEpisodes(id: $playlist, episodes: $episodes) {
				id
			}
		}
	`);

	React.useEffect(() => {
		const onWindowClick = () => setOpen(false);
		window.addEventListener("click", onWindowClick);
		return () => window.removeEventListener("click", onWindowClick);
	}, []);

	if (data === undefined || data.self === null) {
		return null;
	} else if (open && data !== undefined) {
		const eligiblePlaylists = (
			data.self.playlists.filter((playlist) => playlist.episodes.every((episode) => episode.id !== props.episode))
		);

		return (
			<div className={classes(styles.addToPlaylistButton, props.className)}>
				<div className={styles.button}>
					Add to playlist
				</div>
				<div className={styles.dropdown}>
					{
						eligiblePlaylists.length === 0
							? <div className={styles.empty}>No playlists available</div>
							: (
								eligiblePlaylists.map((playlist) => (
									<div
										className={styles.playlist}
										key={playlist.id}
										onClick={async () => {
											await addToPlaylist({
												variables: {
													playlist: playlist.id,
													episodes: (
														playlist.episodes
															.map((episode) => episode.id)
															.concat(props.episode)
													)
												},
											});
											setOpen(false);
											navigate(`/playlist/${playlist.id}?index=${playlist.episodes.length}`);
											await client.resetStore();
										}}
									>
										{playlist.name}
									</div>
								))
							)
					}
				</div>
			</div>
		);
	} else {
		return (
			<div className={classes(styles.addToPlaylistButton, props.className)}>
				<div
					className={styles.button}
					onClick={(event) => {
						setOpen(true);
						event.stopPropagation();
					}}
				>
					Add to playlist
				</div>
			</div>
		);
	}
};

import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./UserPlaylistsPanel.module.scss";

interface Props {
	className?: string;
	id: string;
}

export const UserPlaylistsPanel = (props: Props) => {
	interface PlaylistsResult {
		user: {
			name: string;
			playlists: {
				id: string;
				name: string;
				description: string;
				episodeCount: number;
			}[];
		};
	}

	const { data } = useQuery<PlaylistsResult>(gql`
		query PlaylistsQuery {
			user(id: ${uuidify(props.id)}) {
				name
				playlists {
					id
					name
					description
					episodeCount
				}
			}
		}
	`);

	if (data === undefined) {
		return (
			<Panel
				className={classes(styles.userPlaylistsPanel, props.className)}
				title="Loading..."
			/>
		);
	}

	return (
		<Panel
			className={classes(styles.userPlaylistsPanel, props.className)}
			title={`${data.user.name}'s Playlists`}
		>
			<div className={styles.playlists}>
				{
					data.user.playlists.length === 0
						? (
							<div className={styles.noPlaylists}>
								{data.user.name} has no playlists.
							</div>
						)
						: (
							data.user.playlists.map((playlist) => (
								<div key={playlist.id} className={styles.playlist}>
									<Link className={styles.name} to={`/playlist/${playlist.id}`}>
										{playlist.name}
									</Link>
									<div className={styles.episodeCount}>
										({playlist.episodeCount} episodes)
									</div>
									<div
										className={styles.description}
										dangerouslySetInnerHTML={{ __html: playlist.description }}
									/>
								</div>
							))
						)
				}
			</div>
		</Panel>
	);
};

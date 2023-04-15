import { useLazyQuery, useMutation } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { client } from "@/apollo";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./UpsertPlaylistPanel.module.scss";

interface Props {
	className?: string;
	id?: string;
}

export const UpsertPlaylistPanel = (props: Props) => {
	const [name, setName] = React.useState("");
	const [description, setDescription] = React.useState("");

	const navigate = useNavigate();

	interface PlaylistResult {
		playlist?: {
			id: string;
			name: string;
			description: string;
		}
	}

	const [loadPlaylist, { data }] = useLazyQuery<PlaylistResult>(gql`
		query PlaylistQuery {
			playlist(id: ${uuidify(props.id)}) {
				id
				name
				description
			}
		}
	`);

	const [createPlaylist] = useMutation<{ createPlaylist: { id: string } }>(gql`
		mutation CreatePlaylist {
			createPlaylist(
				name: ${name},
				description: ${description}
			) {
				id
			}
		}
	`);

	const [updatePlaylist] = useMutation<{ updatePlaylist: { id: string } }>(gql`
		mutation UpdatePlaylist {
			updatePlaylist(
				id: ${uuidify(props.id)},
				name: ${name},
				description: ${description}
			) {
				id
			}
		}
	`);

	React.useEffect(() => {
		if (props.id !== undefined) {
			loadPlaylist();
		}
	}, [props.id]);

	React.useEffect(() => {
		if (data?.playlist !== undefined) {
			setName(data.playlist.name);
			setDescription(data.playlist.description);
		}
	}, [data?.playlist]);

	return (
		<Panel
			className={classes(styles.upsertPlaylistPanel, props.className)}
			title={props.id === undefined ? "Add Playlist" : "Edit Playlist"}
		>
			<form
				className={styles.form}
				onSubmit={async (e) => {
					e.preventDefault();
					if (props.id === undefined) {
						const result = await createPlaylist();
						if (result.data?.createPlaylist.id !== undefined) {
							navigate(`/playlist/${result.data.createPlaylist.id}`);
							await client.resetStore();
						}
					} else {
						const result = await updatePlaylist();
						if (result.data?.updatePlaylist.id !== undefined) {
							navigate(`/playlist/${result.data.updatePlaylist.id}`);
							await client.resetStore();
						}
					}
				}}
			>
				<input
					className={styles.input}
					type="text"
					placeholder="Name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>
				<textarea
					className={styles.input}
					placeholder="Description"
					value={description}
					onChange={(e) => setDescription(e.target.value)}
				/>
				<input
					className={styles.submit}
					type="submit"
					value={props.id === undefined ? "Create Playlist" : "Update Playlist"}
					disabled={name === "" || description === ""}
				/>
			</form>
		</Panel>
	);
};
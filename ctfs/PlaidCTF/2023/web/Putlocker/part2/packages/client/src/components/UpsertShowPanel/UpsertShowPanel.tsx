import { useLazyQuery, useMutation } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { client } from "@/apollo";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import { GenresSelector } from "../GenresSelector";

import styles from "./UpsertShowPanel.module.scss";

interface Props {
	className?: string;
	id?: string;
}

export const UpsertShowPanel = (props: Props) => {
	const [name, setName] = React.useState("");
	const [description, setDescription] = React.useState("");
	const [coverUrl, setCoverUrl] = React.useState("");
	const [genres, setGenres] = React.useState<string[]>([]);

	const navigate = useNavigate();

	interface ShowResult {
		show?: {
			id: string;
			name: string;
			description: string;
			coverUrl: string;
			genres: {
				id: string;
				name: string;
			}[];
		}
	}

	const [loadShow, { data }] = useLazyQuery<ShowResult>(gql`
		query ShowQuery {
			show(id: ${uuidify(props.id)}) {
				id
				name
				description: rawDescription
				coverUrl
				genres {
					id
					name
				}
			}
		}
	`);

	const [createShow] = useMutation<{ createShow: { id: string } }>(gql`
		mutation CreateShow {
			createShow(
				name: ${name},
				description: ${description},
				coverUrl: ${coverUrl},
				genres: ${genres}
			) {
				id
			}
		}
	`);

	const [updateShow] = useMutation<{ updateShow: { id: string } }>(gql`
		mutation UpdateShow {
			updateShow(
				id: ${uuidify(props.id)},
				name: ${name},
				description: ${description},
				coverUrl: ${coverUrl},
				genres: ${genres}
			) {
				id
			}
		}
	`);

	React.useEffect(() => {
		if (props.id !== undefined) {
			loadShow();
		}
	}, [props.id]);

	React.useEffect(() => {
		if (data?.show !== undefined) {
			setName(data.show.name);
			setDescription(data.show.description);
			setCoverUrl(data.show.coverUrl);
			setGenres(data.show.genres.map((genre) => genre.id));
		}
	}, [data?.show]);

	return (
		<Panel
			className={classes(styles.upsertShowPanel, props.className)}
			title={props.id === undefined ? "Add Show" : "Edit Show"}
		>
			<form
				className={styles.form}
				onSubmit={async (e) => {
					e.preventDefault();
					if (props.id === undefined) {
						const result = await createShow();
						if (result.data?.createShow.id !== undefined) {
							navigate(`/show/${result.data.createShow.id}`);
							await client.resetStore();
						}
					} else {
						const result = await updateShow();
						if (result.data?.updateShow.id !== undefined) {
							navigate(`/show/${result.data.updateShow.id}`);
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
					className={styles.input}
					type="url"
					placeholder="Cover URL"
					value={coverUrl}
					onChange={(e) => setCoverUrl(e.target.value)}
				/>
				<GenresSelector
					className={styles.genreSelector}
					value={genres}
					onChange={setGenres}
				/>
				<input
					className={styles.submit}
					type="submit"
					value={props.id === undefined ? "Create Show" : "Update Show"}
					disabled={name === "" || description === "" || coverUrl === ""}
				/>
			</form>
		</Panel>
	);
};
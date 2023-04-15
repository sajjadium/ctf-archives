import { useLazyQuery, useMutation, useQuery } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { client } from "@/apollo";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./UpsertEpisodePanel.module.scss";

interface Props {
	className?: string;
	id?: string;
}

export const UpsertEpisodePanel = (props: Props) => {
	const [show, setShow] = React.useState<string | undefined>(undefined);
	const [name, setName] = React.useState("");
	const [description, setDescription] = React.useState("");
	const [url, setUrl] = React.useState("");

	const navigate = useNavigate();

	interface SelfShowResult {
		self: {
			shows: {
				id: string;
				name: string;
			}[];
		};
	}

	const { data: selfShowsData } = useQuery<SelfShowResult>(gql`
		query SelfShowsQuery {
			self {
				shows {
					id
					name
				}
			}
		}
	`);

	interface EpisodeResult {
		episode?: {
			id: string;
			name: string;
			description: string;
			url: string;
			show: {
				id: string;
			};
		}
	}

	const [loadEpisode, { data }] = useLazyQuery<EpisodeResult>(gql`
		query EpisodeQuery {
			episode(id: ${uuidify(props.id)}) {
				id
				name
				description: rawDescription
				url
				show {
					id
				}
			}
		}
	`);

	const [createEpisode] = useMutation<{ createEpisode: { id: string } }>(gql`
		mutation CreateEpisode {
			createEpisode(
				show: ${uuidify(show)},
				name: ${name},
				description: ${description},
				url: ${url}
			) {
				id
			}
		}
	`);

	const [updateEpisode] = useMutation<{ updateEpisode: { id: string } }>(gql`
		mutation UpdateEpisode {
			updateEpisode(
				id: ${uuidify(props.id)},
				name: ${name},
				description: ${description},
				url: ${url}
			) {
				id
			}
		}
	`);

	React.useEffect(() => {
		if (props.id !== undefined) {
			loadEpisode();
		}
	}, [props.id]);

	React.useEffect(() => {
		if (data?.episode !== undefined) {
			setName(data.episode.name);
			setDescription(data.episode.description);
			setUrl(data.episode.url);
			setShow(data.episode.show.id);
		}
	}, [data?.episode]);

	return (
		<Panel
			className={classes(styles.upsertEpisodePanel, props.className)}
			title={props.id === undefined ? "Add Episode" : "Edit Episode"}
		>
			<form
				className={styles.form}
				onSubmit={async (e) => {
					e.preventDefault();
					if (props.id === undefined) {
						const result = await createEpisode();
						if (result.data?.createEpisode.id !== undefined) {
							navigate(`/episode/${result.data.createEpisode.id}`);
							await client.resetStore();
						}
					} else {
						const result = await updateEpisode();
						if (result.data?.updateEpisode.id !== undefined) {
							navigate(`/episode/${result.data.updateEpisode.id}`);
							await client.resetStore();
						}
					}
				}}
			>
				<select
					className={styles.input}
					value={show}
					onChange={(e) => setShow(e.target.value)}
				>
					<option disabled selected value="">Select a show...</option>
					{
						selfShowsData?.self.shows.map((show) => (
							<option key={show.id} value={show.id}>{show.name}</option>
						))
					}
				</select>
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
					placeholder="Video URL"
					value={url}
					onChange={(e) => setUrl(e.target.value)}
				/>
				<input
					className={styles.submit}
					type="submit"
					value={props.id === undefined ? "Create Episode" : "Update Episode"}
					disabled={show === undefined || name === "" || description === "" || url === ""}
				/>
			</form>
		</Panel>
	);
};
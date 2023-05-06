import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./EpisodesPanel.module.scss";

interface Props {
	className?: string;
	show: string;
}

export const EpisodesPanel = (props: Props) => {
	interface EpisodesResult {
		show: {
			episodes: {
				id: string;
				name: string;
			}[];
		}
	}

	const { data, loading, error } = useQuery<EpisodesResult>(gql`
		query EpisodesQuery {
			show(id: ${uuidify(props.show)}) {
				episodes {
					id
					name
				}
			}
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.episodesPanel)}
			title="Episode List"
		>
			{
				loading ? "Loading..." :
				error || data === undefined ? "Error loading episodes" :
				(
					<ul className={styles.episodesList}>
						{
							data.show.episodes.map((episode) => (
								<Link className={styles.link} to={`/episode/${episode.id}`}>
									<li key={episode.id} className={styles.episode}>
										{episode.name}
									</li>
								</Link>
							))
						}
					</ul>
				)
			}
		</Panel>
	);
};

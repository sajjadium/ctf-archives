
import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./RecentPanel.module.scss";

interface Props {
	className?: string;
}

export const RecentPanel = (props: Props) => {
	interface RecentResult {
		recentEpisodes: {
			id: string;
			name: string;
			show: {
				coverUrl: string;
			};
		}[];
	}

	const { data, loading, error } = useQuery<RecentResult>(gql`
		query RecentQuery {
			recentEpisodes {
				id
				name
				show {
					coverUrl
				}
			}
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.recentPanel)}
			title="Recent Releases"
		>
			{
				loading ? "Loading..." :
				error || data === undefined ? "Error loading recent episodes" :
				(
					<div className={styles.recentList}>
						{
							data.recentEpisodes.map((episode) => (
								<Link key={episode.id} className={styles.episode} to={`/episode/${episode.id}`}>
									<img src={episode.show.coverUrl} className={styles.cover} />
									<div className={styles.name}>{episode.name}</div>
								</Link>
							))
						}
					</div>
				)
			}
		</Panel>
	);
};

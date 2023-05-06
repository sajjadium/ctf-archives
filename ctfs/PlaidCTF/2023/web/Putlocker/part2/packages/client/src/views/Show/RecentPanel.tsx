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
		}[];
	}

	const { data, loading, error } = useQuery<RecentResult>(gql`
		query RecentQuery {
			recentEpisodes {
				id
				name
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
				error || data === undefined ? "Error loading ongoing shows" :
				(
					<ul className={styles.recentList}>
						{
							data.recentEpisodes.map((episodes) => (
								<li key={episodes.id} className={styles.episode}>
									<Link className={styles.link} to={`/episode/${episodes.id}`}>
										{episodes.name}
									</Link>
								</li>
							))
						}
					</ul>
				)
			}
		</Panel>
	);
};

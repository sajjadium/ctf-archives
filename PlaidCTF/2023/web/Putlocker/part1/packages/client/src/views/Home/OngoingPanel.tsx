
import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./OngoingPanel.module.scss";

interface Props {
	className?: string;
}

export const OngoingPanel = (props: Props) => {
	interface OngoingResult {
		allShows: {
			id: string;
			name: string;
		}[];
	}

	const { data, loading, error } = useQuery<OngoingResult>(gql`
		query OngoingQuery {
			allShows {
				id
				name
			}
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.ongoingPanel)}
			title="Ongoing & Popular Series"
		>
			{
				loading ? "Loading..." :
				error || data === undefined ? "Error loading ongoing shows" :
				(
					<ul className={styles.ongoingList}>
						{
							data.allShows.map((show) => (
								<li key={show.id} className={styles.show}>
									<Link className={styles.link} to={`/show/${show.id}`}>
										{show.name}
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

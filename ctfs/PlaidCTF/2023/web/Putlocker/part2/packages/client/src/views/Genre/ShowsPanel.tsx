import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./ShowsPanel.module.scss";

interface Props {
	className?: string;
	genre: string;
}

export const ShowsPanel = (props: Props) => {
	interface ShowsResult {
		genre: {
			name: string;
			shows: {
				id: string;
				name: string;
			}[];
		}
	}

	const { data, loading, error } = useQuery<ShowsResult>(gql`
		query ShowsQuery {
			genre(id: ${uuidify(props.genre)}) {
				name
				shows {
					id
					name
				}
			}
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.showsPanel)}
			title="Search By Genre"
		>
			{
				loading ? "Loading..." :
				error || data === undefined ? "Error loading genre" :
				(
					<>
						<div className={styles.title}>
							{data.genre.name} Series
						</div>
						<div className={styles.list}>
							{
								data.genre.shows.map((show) => (
									<Link className={styles.link} to={`/show/${show.id}`}>
										{show.name}
									</Link>
								))
							}
						</div>
					</>
				)
			}
		</Panel>
	);
};
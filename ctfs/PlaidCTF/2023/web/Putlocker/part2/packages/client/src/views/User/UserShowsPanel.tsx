
import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./UserShowsPanel.module.scss";

interface Props {
	className?: string;
	id: string;
}

export const UserShowsPanel = (props: Props) => {
	interface ShowsResult {
		user: {
			name: string;
			shows: {
				id: string;
				name: string;
			}[];
		};
	}

	const { data } = useQuery<ShowsResult>(gql`
		query PlaylistsQuery {
			user(id: ${uuidify(props.id)}) {
				name
				shows {
					id
					name
				}
			}
		}
	`);

	if (data === undefined) {
		return (
			<Panel
				className={classes(styles.userShowsPanel, props.className)}
				title="Loading..."
			/>
		);
	}

	return (
		<Panel
			className={classes(props.className, styles.userShowsPanel)}
			title={`${data.user.name}'s Shows`}
		>
			{
				data.user.shows.length > 0
					? (
						<ul className={styles.showsList}>
							{
								data.user.shows.map((show) => (
									<li key={show.id} className={styles.show}>
										<Link className={styles.link} to={`/show/${show.id}`}>
											{show.name}
										</Link>
									</li>
								))
							}
						</ul>
					)
					: (
						<div className={styles.empty}>
							{`${data.user.name} hasn't uploaded any shows.`}
						</div>
					)
			}
		</Panel>
	);
};

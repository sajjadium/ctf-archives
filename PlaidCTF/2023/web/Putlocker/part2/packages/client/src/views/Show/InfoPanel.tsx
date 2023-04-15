import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { ReportButton } from "@/components/ReportButton";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./InfoPanel.module.scss";

interface Props {
	className?: string;
	id: string;
}

export const InfoPanel = (props: Props) => {
	interface InfoQueryResult {
		show: {
			id: string;
			name: string;
			description: { __html: string };
			coverUrl: string;
			owner: {
				id: string;
			};
			genres: {
				id: string;
				name: string;
			}[];
		};
	}

	const { data, loading, error } = useQuery<InfoQueryResult>(gql`
		query InfoQuery {
			show(id: ${uuidify(props.id)}) {
				id
				name
				description
				coverUrl
				owner {
					id
				}
				genres {
					id
					name
				}
			}
		}
	`);

	const { data: selfData } = useQuery<{ self: { id: string } }>(gql`
		query SelfQuery {
			self {
				id
			}
		}
	`);

	const editLink = (
		selfData?.self?.id !== undefined && selfData?.self?.id === data?.show?.owner?.id
			? (
				<Link className={styles.editLink} to={`/show/${props.id}/edit`}>(Edit)</Link>
			)
			: null
	);


	return (
		<Panel
			className={classes(props.className, styles.infoPanel)}
			title={
				loading ? "Loading..." :
				data === undefined || error ? "Error loading show" :
				<>
					{data.show.name}
					{editLink}
				</>
			}
		>
			{
				!loading && error === undefined && data !== undefined
					? (
						<div className={styles.content}>
							<img src={data.show.coverUrl} className={styles.cover} />
							<div
								className={styles.description}
								dangerouslySetInnerHTML={data.show.description}
							/>
							<div className={styles.genres}>
								<b>Genres:</b>
								{
									data.show.genres.map((genre) => (
										<Link className={styles.genre} to={`/genre/${genre.id}`} key={genre.id}>
											{genre.name}
										</Link>
									))
								}
							</div>
							<ReportButton className={styles.report} />
						</div>
					)
					: null
			}
		</Panel>
	);
};

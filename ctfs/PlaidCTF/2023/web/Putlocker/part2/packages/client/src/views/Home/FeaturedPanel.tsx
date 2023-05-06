import { useQuery } from "@apollo/client";
import React from "react";
import { Link } from "react-router-dom";

import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./FeaturedPanel.module.scss";

interface Props {
	className?: string;
}

export const FeaturedPanel = (props: Props) => {
	interface FeaturedResult {
		featuredShow: {
			id: string;
			name: string;
			description: { __html: string };
			coverUrl: string;
		};
	}

	const { data, loading, error } = useQuery<FeaturedResult>(gql`
		query FeaturedQuery {
			featuredShow {
				id
				name
				description
				coverUrl
			}
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.featuredPanel)}
			title={
				loading ? "Loading..." :
				data === undefined || error ? "Error loading featured show" :
				<Link className={styles.link} to={`/show/${data.featuredShow.id}`}>{data.featuredShow.name}</Link>
			}
		>
			{
				!loading && error === undefined && data !== undefined
					? (
						<div className={styles.content}>
							<img src={data.featuredShow.coverUrl} className={styles.cover} />
							<div
								className={styles.description}
								dangerouslySetInnerHTML={data.featuredShow.description}
							/>
						</div>
					)
					: null
			}
		</Panel>
	);
};

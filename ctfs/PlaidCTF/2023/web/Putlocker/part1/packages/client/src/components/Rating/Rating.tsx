import { useMutation, useQuery } from "@apollo/client";
import React from "react";

import { client } from "@/apollo";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import styles from "./Rating.module.scss";

interface Props {
	className?: string;
	episode: string;
}

export const Rating = (props: Props) => {
	const [userRating, setUserRating] = React.useState<number | undefined>(undefined);

	interface RatingResult {
		episode?: {
			rating: number;
			ratingCount: number;
		};
	}

	const { data } = useQuery<RatingResult>(gql`
		query RatingQuery {
			episode(id: ${uuidify(props.episode)}) {
				rating
				ratingCount
			}
		}
	`);

	const [pushRating] = useMutation(gql`
		mutation PushRating {
			rateEpisode(id: ${uuidify(props.episode)}, rating: ${userRating})
		}
	`);

	const onMouseEvent = React.useCallback((event: React.MouseEvent<HTMLDivElement>) => {
		const rect = event.currentTarget.getBoundingClientRect();
		const x = event.clientX - rect.left;
		setUserRating(Math.ceil(x / rect.width * 5));
	}, []);

	const rating = data?.episode?.rating ?? 0;

	return (
		<div className={classes(styles.rating, props.className)}>
			<div
				className={styles.stars}
				onMouseEnter={onMouseEvent}
				onMouseMove={onMouseEvent}
				onMouseLeave={() => setUserRating(undefined)}
				onClick={async () => {
					if (userRating !== undefined) {
						await pushRating();
						await client.resetStore();
					}
				}}
			>
				<div
					className={styles.averageRating}
					style={{ width: `${rating / 5 * 100}%` }}
				/>
				<div
					className={styles.userRating}
					style={{ width: `${userRating === undefined ? 0 : userRating / 5 * 100}%` }}
				/>
				<div className={styles.overlay} />
			</div>
			<div className={styles.text}>
				{`${rating} / 5 - ${data?.episode?.ratingCount ?? 0} ratings`}
			</div>
		</div>
	);
};

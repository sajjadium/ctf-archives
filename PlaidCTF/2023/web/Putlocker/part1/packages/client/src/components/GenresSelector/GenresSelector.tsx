import { useQuery } from "@apollo/client";
import React from "react";

import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./GenresSelector.module.scss";

interface Props {
	className?: string;
	value: string[];
	onChange: (value: string[]) => void;
}

export const GenresSelector = (props: Props) => {
	interface GenresResult {
		allGenres: {
			id: string;
			name: string;
		}[];
	}

	const { data } = useQuery<GenresResult>(gql`
		query GenresQuery {
			allGenres {
				id
				name
			}
		}
	`);

	if (data === undefined) {
		return null;
	}

	return (
		<div className={classes(styles.genresSelector, props.className)}>
			{
				data.allGenres.map((genre) => (
					<div className={styles.genre} key={genre.id}>
						<input
							className={styles.checkbox}
							type="checkbox"
							checked={props.value.includes(genre.id)}
							onChange={(event) => {
								if (event.target.checked) {
									props.onChange([...props.value, genre.id]);
								} else {
									props.onChange(props.value.filter((id) => id !== genre.id));
								}
							}}
						/>
						<div className={styles.name}>{genre.name}</div>
					</div>
				))
			}
		</div>
	);
};

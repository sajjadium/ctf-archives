import React from "react";
import { useParams } from "react-router";

import { EpisodePanel } from "@/components/EpisodePanel";
import { Promo } from "@/components/Promo";

import { BaseView } from "../BaseView";

import styles from "./Episode.module.scss";

export const Episode = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<BaseView>
			<div className={styles.episode}>
				<EpisodePanel className={styles.episodePanel} id={id} />
				<Promo className={styles.promo} />
			</div>
		</BaseView>
	);
};

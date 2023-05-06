import React from "react";
import { useParams } from "react-router";

import { EnsureLoggedIn } from "@/components/EnsureLoggedIn";
import { UpsertEpisodePanel } from "@/components/UpsertEpisodePanel";

import { BaseView } from "../BaseView";

import styles from "./EditEpisode.module.scss";

export const EditEpisode = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<EnsureLoggedIn fallback="/">
			<BaseView>
				<div className={styles.editEpisode}>
					<UpsertEpisodePanel className={styles.panel} id={id} />
				</div>
			</BaseView>
		</EnsureLoggedIn>
	);
};

import React from "react";
import { useParams } from "react-router";

import { EnsureAdmin } from "@/components/EnsureAdmin";
import { UpsertEpisodePanel } from "@/components/UpsertEpisodePanel";

import { BaseView } from "../BaseView";

import styles from "./EditEpisode.module.scss";

export const EditEpisode = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<EnsureAdmin fallback="/">
			<BaseView>
				<div className={styles.editEpisode}>
					<UpsertEpisodePanel className={styles.panel} id={id} />
				</div>
			</BaseView>
		</EnsureAdmin>
	);
};

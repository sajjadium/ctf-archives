import React from "react";
import { useParams } from "react-router";

import { BaseView } from "../BaseView";
import { EpisodesPanel } from "./EpisodesPanel";
import { InfoPanel } from "./InfoPanel";
import { RecentPanel } from "./RecentPanel";

import styles from "./Show.module.scss";

export const Show = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<BaseView>
			<div className={styles.show}>
				<InfoPanel className={styles.featured} id={id} />
				<EpisodesPanel className={styles.episodes} show={id} />
				<RecentPanel className={styles.recent} />
			</div>
		</BaseView>
	);
};

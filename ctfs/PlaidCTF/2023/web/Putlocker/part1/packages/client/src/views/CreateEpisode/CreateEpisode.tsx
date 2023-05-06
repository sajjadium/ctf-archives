import React from "react";

import { EnsureLoggedIn } from "@/components/EnsureLoggedIn";
import { UpsertEpisodePanel } from "@/components/UpsertEpisodePanel";

import { BaseView } from "../BaseView";

import styles from "./CreateEpisode.module.scss";

export const CreateEpisode = () => (
	<EnsureLoggedIn fallback="/">
		<BaseView>
			<div className={styles.createEpisode}>
				<UpsertEpisodePanel className={styles.panel} />
			</div>
		</BaseView>
	</EnsureLoggedIn>
);

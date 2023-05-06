import React from "react";

import { EnsureAdmin } from "@/components/EnsureAdmin";
import { UpsertEpisodePanel } from "@/components/UpsertEpisodePanel";

import { BaseView } from "../BaseView";

import styles from "./CreateEpisode.module.scss";

export const CreateEpisode = () => (
	<EnsureAdmin fallback="/">
		<BaseView>
			<div className={styles.createEpisode}>
				<UpsertEpisodePanel className={styles.panel} />
			</div>
		</BaseView>
	</EnsureAdmin>
);

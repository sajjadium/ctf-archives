import React from "react";

import { EnsureLoggedIn } from "@/components/EnsureLoggedIn";
import { UpsertShowPanel } from "@/components/UpsertShowPanel";

import { BaseView } from "../BaseView";

import styles from "./CreateShow.module.scss";

export const CreateShow = () => (
	<EnsureLoggedIn fallback="/">
		<BaseView>
			<div className={styles.createShow}>
				<UpsertShowPanel className={styles.panel} />
			</div>
		</BaseView>
	</EnsureLoggedIn>
);

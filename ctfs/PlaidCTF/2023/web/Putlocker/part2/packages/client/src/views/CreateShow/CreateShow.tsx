import React from "react";

import { EnsureAdmin } from "@/components/EnsureAdmin";
import { UpsertShowPanel } from "@/components/UpsertShowPanel";

import { BaseView } from "../BaseView";

import styles from "./CreateShow.module.scss";

export const CreateShow = () => (
	<EnsureAdmin fallback="/">
		<BaseView>
			<div className={styles.createShow}>
				<UpsertShowPanel className={styles.panel} />
			</div>
		</BaseView>
	</EnsureAdmin>
);

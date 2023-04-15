import React from "react";
import { useParams } from "react-router";

import { EnsureLoggedIn } from "@/components/EnsureLoggedIn";
import { UpsertShowPanel } from "@/components/UpsertShowPanel";

import { BaseView } from "../BaseView";

import styles from "./EditShow.module.scss";

export const EditShow = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<EnsureLoggedIn fallback="/">
			<BaseView>
				<div className={styles.editShow}>
					<UpsertShowPanel className={styles.panel} id={id} />
				</div>
			</BaseView>
		</EnsureLoggedIn>
	);
};

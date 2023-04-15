import React from "react";
import { useParams } from "react-router";

import { Promo } from "@/components/Promo";

import { BaseView } from "../BaseView";
import { ShowsPanel } from "./ShowsPanel";

import styles from "./Genre.module.scss";

export const Genre = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<BaseView>
			<div className={styles.genre}>
				<ShowsPanel className={styles.shows} genre={id} />
				<Promo className={styles.promo} />
			</div>
		</BaseView>
	);
};

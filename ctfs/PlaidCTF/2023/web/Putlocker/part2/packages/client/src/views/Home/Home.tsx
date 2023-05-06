import React from "react";

import { BaseView } from "../BaseView";
import { FeaturedPanel } from "./FeaturedPanel";
import { OngoingPanel } from "./OngoingPanel";
import { RecentPanel } from "./RecentPanel";

import styles from "./Home.module.scss";

export const Home = () => (
	<BaseView>
		<div className={styles.home}>
			<FeaturedPanel className={styles.featured} />
			<RecentPanel className={styles.recent} />
			<OngoingPanel className={styles.ongoing} />
		</div>
	</BaseView>
);

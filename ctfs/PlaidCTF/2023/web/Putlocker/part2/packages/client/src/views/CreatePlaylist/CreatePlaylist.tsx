import React from "react";

import { EnsureLoggedIn } from "@/components/EnsureLoggedIn";
import { UpsertPlaylistPanel } from "@/components/UpsertPlaylistPanel";

import { BaseView } from "../BaseView";

import styles from "./CreatePlaylist.module.scss";

export const CreatePlaylist = () => (
	<EnsureLoggedIn fallback="/login">
		<BaseView>
			<div className={styles.createPlaylist}>
				<UpsertPlaylistPanel className={styles.panel} />
			</div>
		</BaseView>
	</EnsureLoggedIn>
);

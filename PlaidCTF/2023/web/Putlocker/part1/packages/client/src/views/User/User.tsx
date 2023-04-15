import React from "react";
import { useParams } from "react-router";

import { BaseView } from "../BaseView";
import { UserPlaylistsPanel } from "./UserPlaylistsPanel";
import { UserShowsPanel } from "./UserShowsPanel";

import styles from "./User.module.scss";

export const User = () => {
	const params = useParams();
	const id = params.id as string;

	return (
		<BaseView>
			<div className={styles.user}>
				<UserPlaylistsPanel className={styles.playlists} id={id} />
				<UserShowsPanel className={styles.shows} id={id} />
			</div>
		</BaseView>
	);
};

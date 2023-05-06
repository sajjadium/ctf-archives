import React from "react";

import { BaseView } from "../BaseView";
import { LoginPanel } from "./LoginPanel";

import styles from "./Login.module.scss";

export const Login = () => (
	<BaseView>
		<div className={styles.login}>
			<LoginPanel className={styles.loginPanel} />
		</div>
	</BaseView>
);

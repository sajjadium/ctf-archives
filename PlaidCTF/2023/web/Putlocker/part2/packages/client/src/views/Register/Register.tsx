import React from "react";

import { BaseView } from "../BaseView";
import { RegisterPanel } from "./RegisterPanel";

import styles from "./Register.module.scss";

export const Register = () => (
	<BaseView>
		<div className={styles.register}>
			<RegisterPanel className={styles.registerPanel} />
		</div>
	</BaseView>
);

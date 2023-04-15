import React from "react";

import { classes } from "@/utils/css";

import styles from "./Panel.module.scss";

interface Props {
	className?: string;
	title: React.ReactNode;
	children?: React.ReactNode;
}

export const Panel = (props: Props) => (
	<div className={classes(styles.panel, props.className)}>
		<div className={styles.title}>
			{props.title}
		</div>
		<div className={styles.content}>
			{props.children}
		</div>
	</div>
);
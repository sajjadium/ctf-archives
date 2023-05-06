import React from "react";

import { classes } from "@/utils/css.js";

import styles from "./OutlineText.module.scss";

interface Props {
	className?: string;
	children: React.ReactNode;
	onMouseEnter?: () => void;
	onMouseLeave?: () => void;
}

export const OutlineText = (props: Props) => (
	<span
		className={classes(
			styles.outlineText,
			props.className
		)}
		onMouseEnter={props.onMouseEnter}
		onMouseLeave={props.onMouseLeave}
	>
		{props.children}
		<span className={styles.outline}>
			{props.children}
		</span>
	</span>
);

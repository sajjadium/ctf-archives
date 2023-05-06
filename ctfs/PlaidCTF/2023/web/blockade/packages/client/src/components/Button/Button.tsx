import React from "react";

import { classes } from "@/utils/css.js";

import styles from "./Button.module.scss";

interface Props {
	className?: string;
	onClick?: (event: React.MouseEvent<HTMLDivElement>) => void;
	children: React.ReactNode;
}

export const Button = (props: Props) => (
	<div
		className={classes(styles.button, props.className)}
		onClick={props.onClick}
	>
		{props.children}
	</div>
);

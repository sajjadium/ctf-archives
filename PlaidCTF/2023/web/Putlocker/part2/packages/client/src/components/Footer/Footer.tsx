import React from "react";

import { classes } from "@/utils/css";

import styles from "./Footer.module.scss";

interface Props {
	className?: string;
}

export const Footer = (props: Props) => (
	<footer className={classes(styles.footer, props.className)}>
		&#9413;2023.  "Designed" for Davy Jones' Putlocker.
	</footer>
);

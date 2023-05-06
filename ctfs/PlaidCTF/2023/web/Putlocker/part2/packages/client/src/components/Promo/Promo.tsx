import PlaidPlus from "@assets/plaidplus.png";
import React from "react";

import { classes } from "@/utils/css";

import styles from "./Promo.module.scss";

interface Props {
	className?: string;
}

export const Promo = (props: Props) => (
	<a
		className={classes(styles.promo, props.className)}
		href="https://2021.archive.plaidctf.com"
		target="_blank"
	>
		<img className={styles.logo} src={PlaidPlus} />
		<div className={styles.text}>
			<p>Pwnables, reverse engineering, web, crypto, and more.</p>
			<p>Starting at only $5/month.</p>
		</div>
	</a>
);

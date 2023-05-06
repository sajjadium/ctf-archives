import React from "react";

import { MovementToken } from "@puzzled/types";

import { classes } from "@/utils/css.js";

import styles from "./Token.module.scss";

interface Props {
	className?: string;
	kind: MovementToken;
}

export const Token = (props: Props) => (
	<div
		className={classes(
			styles.token,
			props.className,
			(
				props.kind === MovementToken.Forward ? styles.forward :
				props.kind === MovementToken.Left ? styles.left :
				props.kind === MovementToken.Right ? styles.right :
				undefined
			)
		)}
	/>
);

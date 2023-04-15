import React from "react";

import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";

import styles from "./BaseView.module.scss";

interface Props {
	children?: React.ReactNode;
}

export const BaseView = (props: Props) => (
	<div className={styles.baseView}>
		<Header className={styles.header} />
		<div className={styles.content}>
			{props.children}
		</div>
		<Footer className={styles.footer} />
	</div>
);

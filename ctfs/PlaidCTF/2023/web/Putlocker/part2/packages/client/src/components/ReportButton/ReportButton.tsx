import { useMutation } from "@apollo/client";
import React from "react";
import { useLocation } from "react-router";

import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./ReportButton.module.scss";

interface Props {
	className?: string;
}

export const ReportButton = (props: Props) => {
	const _location = useLocation(); // used to subscribe to location changes
	const [reported, setReported] = React.useState(false);

	const [report] = useMutation(gql`
		mutation Report {
			report(url: ${window.location.href})
		}
	`);

	return (
		<div
			className={classes(
				styles.reportButton,
				reported ? styles.reported : undefined,
				props.className
			)}
			onClick={() => {
				report();
				setReported(true);
			}}
		>
			{reported ? "Reported" : "Report"}
		</div>
	);
};

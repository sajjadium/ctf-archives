
import { useMutation } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router-dom";

import { client } from "@/apollo";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./RegisterPanel.module.scss";

interface Props {
	className?: string;
}

export const RegisterPanel = (props: Props) => {
	const [name, setName] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [confirmPassword, setConfirmPassword] = React.useState("");

	const navigate = useNavigate();

	const [register] = useMutation<{ register: string }>(gql`
		mutation Register {
			register(name: ${name}, password: ${password})
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.registerPanel)}
			title="Log-In"
		>
			<form
				className={styles.form}
				onSubmit={async (e) => {
					e.preventDefault();
					const result = await register();
					if (result.data?.register !== undefined) {
						localStorage.setItem("token", result.data.register);
						navigate("/");
						await client.resetStore();
					}
				}}
			>
				<input
					className={styles.input}
					type="text"
					placeholder="Username"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>
				<input
					className={styles.input}
					type="password"
					placeholder="Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				<input
					className={styles.input}
					type="password"
					placeholder="Confirm Password"
					value={confirmPassword}
					onChange={(e) => setConfirmPassword(e.target.value)}
				/>
				<input
					className={styles.submit}
					type="submit"
					value="Register"
					disabled={password !== confirmPassword}
				/>
			</form>
		</Panel>
	);
};

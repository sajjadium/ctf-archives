
import { useMutation } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { client } from "@/apollo";
import { Panel } from "@/components/Panel";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./LoginPanel.module.scss";

interface Props {
	className?: string;
}

export const LoginPanel = (props: Props) => {
	const [name, setName] = React.useState("");
	const [password, setPassword] = React.useState("");

	const navigate = useNavigate();

	const [login] = useMutation<{ login: string }>(gql`
		mutation Login {
			login(name: ${name}, password: ${password})
		}
	`);

	return (
		<Panel
			className={classes(props.className, styles.loginPanel)}
			title="Log-In"
		>
			<form
				className={styles.form}
				onSubmit={async (e) => {
					e.preventDefault();
					const result = await login();
					if (result.data?.login !== undefined) {
						localStorage.setItem("token", result.data.login);
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
					className={styles.submit}
					type="submit"
					value="Log-In"
				/>
			</form>
		</Panel>
	);
};

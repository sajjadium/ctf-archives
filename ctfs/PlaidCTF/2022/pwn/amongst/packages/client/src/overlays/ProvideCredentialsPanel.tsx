import React from "react";

import { Game, ProvideCredentialsController } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./ProvideCredentialsPanel.module.scss";

interface Props {
	game: Game;
	controller: ProvideCredentialsController;
}

export const ProvideCredentialsPanel = (props: Props) => {
	const [username, setUsername] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [loading, setLoading] = React.useState(false);
	const [frameCount, setFrameCount] = React.useState(0);
	const [closing, setClosing] = React.useState(false);

	useFrame(() => {
		setFrameCount((fc) => fc + 1);
	});

	const close = () => {
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	React.useEffect(() => {
		setLoading(false);
	}, [props.controller.lastResponse]);

	React.useEffect(() => {
		if (props.controller.state.complete) {
			const timeout = setTimeout(close, 5000);
			return () => clearTimeout(timeout);
		}
	}, [props.controller.state.complete]);

	return (
		<div
			className={classes(
				styles.provideCredentialsPanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background}></div>
			<div className={styles.panel}>
				<button
					className={styles.close}
					onClick={() => {
						if (closing) {
							return;
						}

						close();
					}}
				/>
				<div className={styles.postIt}>
					<div>My login:</div>
					<div>{props.controller.state.credentials.username}</div>
					<div>{props.controller.state.credentials.password}</div>
				</div>
				<input
					type="text"
					placeholder="Username"
					className={classes(styles.input, styles.username)}
					value={username}
					onChange={(e) => setUsername(e.target.value)}
				/>
				<input
					type="password"
					placeholder="Password"
					className={classes(styles.input, styles.password)}
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				<button
					className={styles.login}
					disabled={loading}
					onClick={() => {
						setLoading(true);
						props.controller.send(username, password);
					}}
				/>
				<div className={styles.response}>
					{
						props.controller.lastResponse !== undefined
							? props.controller.lastResponse.message
							: ""
					}
				</div>
			</div>
		</div>
	);
};

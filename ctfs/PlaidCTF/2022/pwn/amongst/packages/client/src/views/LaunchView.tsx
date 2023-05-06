import React from "react";

import styles from "./LaunchView.module.scss";

interface Props {
	onJoinGame: (info: { id: string; host?: string; port: number; name: string }) => void;
}

export const LaunchView = (props: Props) => {
	const [name, setName] = React.useState("");
	const [gameId, setGameId] = React.useState("");
	const [loading, setLoading] = React.useState(false);

	const normalizeName = (n: string) => n.replace(/[^\x20-\x7e]/g, "").substring(0, 20);

	React.useEffect(() => {
		const storedName = localStorage.getItem("name");

		if (storedName !== null) {
			setName(normalizeName(storedName));
		}
	}, []);

	React.useEffect(() => {
		localStorage.setItem("name", name);
	}, [name]);

	return (
		<div className={styles.launchView}>
			<div className={styles.title}>Amongst Ourselves</div>
			<input
				className={styles.name}
				type="text"
				value={name}
				onChange={(evt) => setName(normalizeName(evt.target.value))}
				placeholder="Player Name"
			/>
			<div className={styles.divider} />
			<div className={styles.createGame}>
				<button
					onClick={async () => {
						if (loading) {
							return;
						}

						setLoading(true);

						try {
							const response = await fetch("/api/create", { method: "POST" });
							const json = await response.json() as { id: string; host: string; port: number };
							props.onJoinGame({ id: json.id, host: json.host, port: json.port, name });
						} catch {
							setLoading(false);
						}
					}}
				>
					Create Game
				</button>
			</div>
			<div className={styles.joinGame}>
				<input
					className={styles.gameCode}
					type="text"
					value={gameId}
					onChange={(e) => setGameId(e.target.value)}
					placeholder="Room Code"
				/>
				<button
					onClick={async () => {
						if (loading) {
							return;
						}

						setLoading(true);

						try {
							const response = await fetch(`/api/info/${gameId}`, { method: "GET" });

							if (!response.ok) {
								throw new Error("fail");
							}

							const json = await response.json() as { id: string; host: string; port: number };
							props.onJoinGame({ id: gameId, host: json.host, port: json.port, name });
						} catch {
							setLoading(false);
						}
					}}
				>
					Join Game
				</button>
			</div>
		</div>
	);
};

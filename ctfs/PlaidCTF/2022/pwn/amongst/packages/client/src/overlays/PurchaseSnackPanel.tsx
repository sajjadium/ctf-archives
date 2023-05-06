import React from "react";

import { Game, PurchaseSnackController } from "@amongst/game-client";

import { useFrame } from "../hooks/useFrame";
import { classes } from "../utils/css";

import styles from "./PurchaseSnackPanel.module.scss";

interface Props {
	game: Game;
	controller: PurchaseSnackController;
}

export const PurchaseSnackPanel = (props: Props) => {
	const [value, setValue] = React.useState<string | undefined>("");
	const [frameCount, setFrameCount] = React.useState(0);
	const [autoCloseCancelled, setAutoCloseCancelled] = React.useState(false);
	const [closing, setClosing] = React.useState(false);

	React.useEffect(() => {
		(window as any).setVendingMachineInput = setValue; // you're welcome

		return () => {
			(window as any).setVendingMachineInput = undefined;
		};
	}, []);

	const close = () => {
		setAutoCloseCancelled(true);
		setClosing(true);

		setTimeout(() => {
			props.controller.exit(props.game, props.game.self);
		}, 400);
	};

	useFrame(() => {
		setFrameCount(frameCount + 1);
	});

	React.useEffect(() => {
		if (props.controller.state.complete && !autoCloseCancelled) {
			const timeout = setTimeout(close, 4000);
			return () => clearTimeout(timeout);
		}
	}, [props.controller.state.complete, autoCloseCancelled]);

	return (
		<div
			className={classes(
				styles.purchaseSnackPanel,
				frameCount === 0 || closing ? styles.hidden : undefined
			)}
		>
			<div className={styles.background} />
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
				{
					props.controller.layout?.entrySeq().map(([key, snack]) => (
						<div
							className={classes(
								styles.snack,
								(
									snack === "Potato Chips" ? styles.potatoChips :
									snack === "Chocolate Bar" ? styles.chocolateBar :
									snack === "Chocolate Candy" ? styles.chocolateCandy :
									snack === "Cookies" ? styles.cookies :
									snack === "Peanut Butter Cups" ? styles.peanutButterCups :
									undefined
								)
							)}
							style={{
								left: (key.charCodeAt(1) - 0x31) * 58 + 45,
								top: (key.charCodeAt(0) - 0x41) * 90 + 150,
							}}
						/>
					))
				}
				<div
					className={classes(
						styles.topLayer,
						props.controller.layout !== undefined ? styles.withSnacks : undefined
					)}
				/>
				<div className={styles.display}>{value ?? props.controller.display}</div>
				<div
					className={styles.button}
					style={{
						left: 314,
						top: 195
					}}
					onClick={() => {
						setValue((value ?? "") + "A");
					}}
				>
					A
				</div>
				<div
					className={styles.button}
					style={{
						left: 314,
						top: 230
					}}
					onClick={() => {
						setValue((value ?? "") + "B");
					}}
				>
					B
				</div>
				<div
					className={styles.button}
					style={{
						left: 314,
						top: 265
					}}
					onClick={() => {
						setValue((value ?? "") + "C");
					}}
				>
					C
				</div>
				<div
					className={classes(styles.button, styles.vend)}
					style={{
						left: 314,
						top: 300
					}}
					onClick={() => {
						if (!props.controller.waiting && value !== undefined) {
							props.controller.send(value);
							setValue(undefined);
							props.controller.display = undefined;
						}
					}}
				>
					VEND
				</div>
				<div
					className={styles.button}
					style={{
						left: 354,
						top: 195
					}}
					onClick={() => {
						setValue((value ?? "") + "1");
					}}
				>
					1
				</div>
				<div
					className={styles.button}
					style={{
						left: 354,
						top: 230
					}}
					onClick={() => {
						setValue((value ?? "") + "2");
					}}
				>
					2
				</div>
				<div
					className={styles.button}
					style={{
						left: 354,
						top: 265
					}}
					onClick={() => {
						setValue((value ?? "") + "3");
					}}
				>
					3
				</div>
				<div
					className={styles.button}
					style={{
						left: 354,
						top: 300
					}}
					onClick={() => {
						setValue((value ?? "") + "4");
					}}
				>
					4
				</div>
				{
					props.controller.dispensedSnacks.map((snack, i) => (
						<div
							key={i}
							className={classes(
								styles.snack,
								(
									snack === "Potato Chips" ? styles.potatoChips :
									snack === "Chocolate Bar" ? styles.chocolateBar :
									snack === "Chocolate Candy" ? styles.chocolateCandy :
									snack === "Cookies" ? styles.cookies :
									snack === "Peanut Butter Cups" ? styles.peanutButterCups :
									undefined
								)
							)}
							style={{
								left: 100 + ((i * 163 + 36) % 275),
								top: 506,
								transform: `translate(-50%, -50%) rotate(${(i * 231 + 45) % 360}deg)`
							}}
						/>
					))
				}
				<div className={styles.postIt}>
					<div>I want:</div>
					<div className={styles.desiredSnack}>{props.controller.state.desiredSnack}</div>
				</div>
			</div>
		</div>
	);
};

import React from "react";

import {
	ConspiracyController,
	EmergencyButtonController,
	FileTransferController,
	HoldController,
	MeetingController,
	MovementController,
	ProcessSampleController,
	ProvideCredentialsController,
	PurchaseSnackController,
	RecalibrateEngineController,
	ResetController,
	SatelliteController,
	SettingsController,
	VentController
} from "@amongst/game-client";
import { MsPerTick } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import Dropship from "/assets/dropship.png";
import ShelldLight from "/assets/shelld.png";
import ShelldDark from "/assets/shelld-overlay.png";

import { Body } from "../components/Body";
import { Device } from "../components/Device";
import { Player } from "../components/Player";
import { ShadowDevice } from "../components/ShadowDevice";
import { TaskList } from "../components/TaskList";
import { VisibilityMask } from "../components/VisibilityMask";
import { Wayfinder } from "../components/Wayfinder";
import { ColorFilterProvider } from "../hooks/useColorFilter";
import { useFrame } from "../hooks/useFrame";
import { GameProvider, useGame } from "../hooks/useGame";
import { useKeyboard, useKeyboardTrigger } from "../hooks/useKeyboard";
import { PartialTickContext } from "../hooks/usePartialTick";
import { ShadowFilterProvider } from "../hooks/useShadowFilter";
import { SocketProvider, useSocket } from "../hooks/useSocket";
import { ConspiracyPanel } from "../overlays/ConspiracyPanel";
import { EmergencyButtonPanel } from "../overlays/EmergencyButtonPanel";
import { FileTransferPanel } from "../overlays/FileTransferPanel";
import { HoldOverlay } from "../overlays/HoldOverlay";
import { MeetingPanel } from "../overlays/MeetingPanel";
import { ProcessSamplePanel } from "../overlays/ProcessSamplePanel";
import { ProvideCredentialsPanel } from "../overlays/ProvideCredentialsPanel";
import { PurchaseSnackPanel } from "../overlays/PurchaseSnackPanel";
import { RecalibrateEnginePanel } from "../overlays/RecalibrateEnginePanel";
import { ResetPanel } from "../overlays/ResetPanel";
import { SatellitePanel } from "../overlays/SatellitePanel";
import { SettingsPanel } from "../overlays/SettingsPanel";
import { VentOverlay } from "../overlays/VentOverlay";
import { PixelsPerUnit } from "../utils/constants";
import { classes } from "../utils/css";

import styles from "./GameView.module.scss";

const DesiredLeadTicks = 1;
const MaxAbsoluteDeltaAdjustment = 0.1;

interface Props {
	gameId: string;
	host?: string;
	port: number;
	name: string;
}

export const GameView = (props: Props) => (
	<SocketProvider gameId={props.gameId} host={props.host} port={props.port} name={props.name}>
		<GameProvider>
			<GameViewInner gameId={props.gameId} />
		</GameProvider>
	</SocketProvider>
);

export const GameViewInner = (props: { gameId: string }) => {
	const { ping, socket } = useSocket();
	const [_frameCount, setFrameCount] = React.useState(0); // This serves no purpose other than forcing a rerender
	const [lastTickRollover, setLastTickRollover] = React.useState(0);
	const game = useGame();
	const keyboard = useKeyboard();
	const keyboardTrigger = useKeyboardTrigger(lastTickRollover);

	useFrame((msDelta) => {
		let tickDelta = msDelta / MsPerTick;

		if (game === undefined) {
			return;
		}

		// Adjust the delta slightly to push it closer to the desired lead time.
		const clampedPing = Math.min(ping, 1000);
		const estimatedServerTick = game.partialTick + (Date.now() - (game.lastUpdate - clampedPing / 2)) / MsPerTick;
		const clientTick = game.self.tick + tickDelta;
		const desiredClientTick = estimatedServerTick + DesiredLeadTicks;
		const difference = desiredClientTick - clientTick;
		const deltaAdjustment = Math.min(
			MaxAbsoluteDeltaAdjustment,
			Math.max(
				-MaxAbsoluteDeltaAdjustment,
				difference / 2
			)
		);

		tickDelta += deltaAdjustment;

		const initialPlayerTick = game.self.tick;

		// Pass keyboard info to the current controller if needed.
		if (game.self.controller instanceof MovementController) {
			const leftPressed = keyboard.has("ArrowLeft") || keyboard.has("KeyA");
			const rightPressed = keyboard.has("ArrowRight") || keyboard.has("KeyD");
			const upPressed = keyboard.has("ArrowUp") || keyboard.has("KeyW");
			const downPressed = keyboard.has("ArrowDown") || keyboard.has("KeyS");
			const spacePressed = keyboardTrigger.has("Space");
			const kPressed = keyboardTrigger.has("KeyK");
			const rPressed = keyboardTrigger.has("KeyR");

			const inputDirection = new Point(
				(leftPressed ? -1 : 0) + (rightPressed ? 1 : 0),
				(upPressed ? -1 : 0) + (downPressed ? 1 : 0)
			).unit();

			game.self.controller.advance(game, game.self, tickDelta, inputDirection, spacePressed, kPressed, rPressed);
		} else {
			game.self.controller.advance(game, game.self, tickDelta);
		}

		const finalPlayerTick = game.self.tick;

		if (Math.floor(finalPlayerTick) > Math.floor(initialPlayerTick)) {
			setLastTickRollover(finalPlayerTick);
		}

		setFrameCount((fc) => fc + 1);
	});

	if (game === undefined) {
		return null;
	}

	const selfLocation = (
		game.self.controller instanceof MovementController
			? game.self.controller.displayLocation
			: game.self.location
	);
	const selfVisualState = (
		game.self.controller instanceof MovementController
			? game.self.controller.displayVisualState
			: game.self.visualState
	);

	const overlay = (
		game.self.controller instanceof SettingsController
			? (
				<SettingsPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof ResetController
			? (
				<ResetPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof MeetingController
			? (
				<MeetingPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof EmergencyButtonController
			? (
				<EmergencyButtonPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof FileTransferController
			? (
				<FileTransferPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof ProcessSampleController
			? (
				<ProcessSamplePanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof ProvideCredentialsController
			? (
				<ProvideCredentialsPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof PurchaseSnackController
			? (
				<PurchaseSnackPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof RecalibrateEngineController
			? (
				<RecalibrateEnginePanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof VentController
			? (
				<VentOverlay
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof ConspiracyController
			? (
				<ConspiracyPanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof SatelliteController
			? (
				<SatellitePanel
					game={game}
					controller={game.self.controller}
				/>
			) :
		game.self.controller instanceof HoldController
			? (
				<HoldOverlay
					game={game}
					controller={game.self.controller}
				/>
			) :
		null
	);

	return (
		<div className={styles.gameView}>
			<div
				className={classes(
					styles.disconnectWarning,
					socket.disconnected ?? false ? styles.visible : styles.hidden
				)}
			>
				Disconnected from the server!  Reload to start a new game.
			</div>
			<TaskList game={game} />
			<ColorFilterProvider>
				<ShadowFilterProvider>
					<div className={styles.gameArea}>
						<div
							className={styles.display}
							style={{
								transform: `
									translate(
										${-selfLocation.x * PixelsPerUnit}px,
										${-selfLocation.y * PixelsPerUnit}px
									)
								`
							}}
						>
							<div className={styles.dark}>
								<img
									className={styles.mapImage}
									src={getDarkImage(game.level.map.graphics.id)}
									style={{
										transform: `
											translate(
												${-game.level.map.graphics.origin.x}px,
												${-game.level.map.graphics.origin.y}px
											)
											scale(${1 / game.level.map.graphics.scale})
										`
									}}
								/>
								{
									[...game.level.map.devices.values()]
										.filter((device) => device.graphics?.hideInDark !== true)
										.map((device) => (
											<ShadowDevice key={device.id} device={device} />
										))
								}
							</div>
							<VisibilityMask
								disable={game.self.dead}
								level={game.level}
								graphics={game.level.map.graphics}
								selfLocation={selfLocation}
							>
								<img
									className={styles.mapImage}
									src={getLightImage(game.level.map.graphics.id)}
									style={{
										transform: `
											translate(
												${-game.level.map.graphics.origin.x}px,
												${-game.level.map.graphics.origin.y}px
											)
											scale(${1 / game.level.map.graphics.scale})
										`
									}}
								/>
								<Player.Self
									tick={game.self.tick}
									name={game.self.name}
									color={game.self.color}
									location={selfLocation}
									visualState={selfVisualState}
									dead={game.self.dead}
									hoaxer={game.self.hoaxer}
								/>
								<PartialTickContext.Provider
									value={Math.min(1, (Date.now() - game.lastUpdate) / MsPerTick)}
								>
									{
										[...game.others.values()].map((player) => (
											player.location !== undefined && player.visualState !== undefined
												? (
													<Player.Other
														tick={game.tick}
														key={player.id}
														name={player.name}
														color={player.color}
														location={player.location}
														visualState={player.visualState}
														dead={player.dead}
														hoaxer={player.hoaxer}
													/>
												)
												: undefined
										))
									}
									{
										[...game.bodies.values()].map((body) => (
											<Body
												key={body.id}
												color={body.color}
												location={body.location}
											/>
										))
									}
								</PartialTickContext.Provider>
								{
									[...game.level.map.devices.values()].map((device) => (
										<Device
											key={device.id}
											device={device}
											selfLocation={selfLocation}
											bound={game.level.getSystemForDevice(device.id) !== undefined}
										/>
									))
								}
							</VisibilityMask>
							{
								game.level.systems.valueSeq().map((system) => (
									<Wayfinder
										key={system.id}
										game={game}
										system={system}
										selfLocation={selfLocation}
									/>
								))
							}
						</div>
						{overlay}
						{
							game.level.map.id === "dropship"
								? <div className={styles.roomCode}>Room code: {props.gameId}</div>
								: undefined
						}
					</div>
				</ShadowFilterProvider>
			</ColorFilterProvider>
		</div>
	);
};

function getLightImage(id: string) {
	switch (id) {
		case "shelld": return ShelldLight;
		case "dropship": return Dropship;
		default: return "wat";
	}
}

function getDarkImage(id: string) {
	switch (id) {
		case "shelld": return ShelldDark;
		case "dropship": return Dropship;
		default: return "wat";
	}
}

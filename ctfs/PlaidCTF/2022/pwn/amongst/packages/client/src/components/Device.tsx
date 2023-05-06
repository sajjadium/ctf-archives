import React from "react";

import { Device as GameDevice } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import AccessPoint from "/assets/access-point.png";
import AccessPointSpritesheet from "/assets/access-point-spritesheet.json";
import Centrifuge from "/assets/centrifuge-overworld.png";
import CentrifugeSpritesheet from "/assets/centrifuge-overworld-spritesheet.json";
import ConspiracyBoard from "/assets/conspiracy-board-overworld.png";
import ConspiracyBoardSpritesheet from "/assets/conspiracy-board-overworld-spritesheet.json";
import EmergencyButton from "/assets/emergency-button.png";
import EmergencyButtonSpritesheet from "/assets/emergency-button-spritesheet.json";
import Keypad from "/assets/keypad-overworld.png";
import KeypadSpritesheet from "/assets/keypad-overworld-spritesheet.json";
import Monitor from "/assets/monitor.png";
import MonitorSpritesheet from "/assets/monitor-spritesheet.json";
import Satellite from "/assets/satellite.png";
import SatelliteSpritesheet from "/assets/satellite-spritesheet.json";
import StartPanel from "/assets/start-panel.png";
import StartPanelSpritesheet from "/assets/start-panel-spritesheet.json";
import VendingMachine from "/assets/vending-machine.png";
import VendingMachineSpritesheet from "/assets/vending-machine-spritesheet.json";
import Vent from "/assets/vent.png";
import VentSpritesheet from "/assets/vent-spritesheet.json";

import { Sprite } from "./Sprite";

interface Props {
	device: GameDevice;
	selfLocation?: Point;
	filter?: string;
	bound?: boolean;
}

export const Device = (props: Props) => {
	const colliding = (
		props.bound === true
		&& props.selfLocation !== undefined
		&& props.device.hitArea.contains(props.selfLocation)
	);
	const box = props.device.getBoundingBox();

	if (props.device.graphics !== undefined) {
		const spritesheet = (
			props.device.graphics.type === "vending-machine" ? VendingMachineSpritesheet :
			props.device.graphics.type === "emergency-button" ? EmergencyButtonSpritesheet :
			props.device.graphics.type === "vent" ? VentSpritesheet :
			props.device.graphics.type === "keypad" ? KeypadSpritesheet :
			props.device.graphics.type === "monitor" ? MonitorSpritesheet :
			props.device.graphics.type === "access-point" ? AccessPointSpritesheet :
			props.device.graphics.type === "centrifuge" ? CentrifugeSpritesheet :
			props.device.graphics.type === "conspiracy-board" ? ConspiracyBoardSpritesheet :
			props.device.graphics.type === "start-panel" ? StartPanelSpritesheet :
			props.device.graphics.type === "satellite" ? SatelliteSpritesheet :
			undefined
		);

		const sprite = (
			props.device.graphics.type === "vending-machine" ? VendingMachine :
			props.device.graphics.type === "emergency-button" ? EmergencyButton :
			props.device.graphics.type === "vent" ? Vent :
			props.device.graphics.type === "keypad" ? Keypad :
			props.device.graphics.type === "monitor" ? Monitor :
			props.device.graphics.type === "access-point" ? AccessPoint :
			props.device.graphics.type === "centrifuge" ? Centrifuge :
			props.device.graphics.type === "conspiracy-board" ? ConspiracyBoard :
			props.device.graphics.type === "start-panel" ? StartPanel :
			props.device.graphics.type === "satellite" ? Satellite :
			undefined
		);

		if (spritesheet !== undefined && sprite !== undefined) {
			const frame = spritesheet.frames[colliding ? "highlighted" : "normal"];
			return (
				<Sprite
					frame={frame.frame}
					anchor={frame.anchor}
					position={props.device.graphics.location}
					url={sprite}
					layer={props.device.graphics.layer}
					filter={props.filter}
				/>
			);
		}
	}

	return null;
};

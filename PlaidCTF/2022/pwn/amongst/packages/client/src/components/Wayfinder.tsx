import React from "react";

import { Game } from "@amongst/game-client";
import { SystemKind, SystemState } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

import Arrow from "/assets/arrow.png";
import ArrowSpritesheet from "/assets/arrow-spritesheet.json";

import { PixelsPerUnit } from "../utils/constants";
import { Sprite } from "./Sprite";

interface Props {
	game: Game;
	system: SystemState;
	selfLocation: Point;
}

export const Wayfinder = (props: Props) => {
	const [windowSize, setWindowSize] = React.useState(Math.min(window.innerWidth, window.innerHeight));

	React.useEffect(() => {
		const handleResize = () => {
			setWindowSize(Math.min(window.innerWidth, window.innerHeight));
		};

		window.addEventListener("resize", handleResize);
		return () => window.removeEventListener("resize", handleResize);
	}, []);

	if (!shouldShowWayfinder(props.system)) {
		return null;
	}

	const frame = ArrowSpritesheet.frames.normal;

	return (
		<>
			{
				props.system.devices.map((deviceId) => {
					const device = props.game.level.map.devices.get(deviceId);

					if (device === undefined || device.graphics === undefined) {
						return undefined;
					}

					const r = (windowSize - 40) / PixelsPerUnit / 2;
					const p = props.selfLocation;
					const q = device.graphics.location;
					const v = q.sub(p);
					const u = v.unit();
					const dist = v.mag();
					const renderDist = Math.min(dist - 1, r);
					const pos = p.add(u.scale(renderDist));
					const scale = Math.min(Math.max((dist - 3) / 20, 0), 0.5);

					return (
						<Sprite
							key={deviceId}
							frame={frame.frame}
							anchor={frame.anchor}
							position={pos}
							url={Arrow}
							layer={5}
							rotation={v.ang()}
							scale={scale}
						/>
					);
				})
			}
		</>
	);
};

function shouldShowWayfinder(system: SystemState): boolean {
	switch (system.kind) {
		case SystemKind.ProvideCredentials: return !system.complete;
		case SystemKind.FileTransfer: return !system.uploadComplete;
		case SystemKind.ProcessSample: return !system.taskComplete;
		case SystemKind.RecalibrateEngine: return !system.complete;
		case SystemKind.PurchaseSnack: return !system.complete;
		default: return false;
	}
}

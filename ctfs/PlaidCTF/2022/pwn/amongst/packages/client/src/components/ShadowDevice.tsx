import React from "react";

import { Device as GameDevice } from "@amongst/game-common";

import { useShadowFilter } from "../hooks/useShadowFilter";
import { Device } from "./Device";

interface Props {
	device: GameDevice;
}

export const ShadowDevice = (props: Props) => {
	const shadowFilter = useShadowFilter();

	return (
		<Device
			device={props.device}
			filter={shadowFilter}
		/>
	);
};

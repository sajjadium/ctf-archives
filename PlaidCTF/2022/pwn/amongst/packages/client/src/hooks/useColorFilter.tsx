import React from "react";

import { Color } from "@amongst/game-common";

import { getSpotColors } from "../utils/color";
import { useUniqueId } from "./useUniqueId";

const ColorFilterContext = React.createContext<string | undefined>(undefined);

const VisorColor = 0x96cadd;
const r = (value: number) => ((value >> 16) & 0xff) / 255;
const g = (value: number) => ((value >> 8) & 0xff) / 255;
const b = (value: number) => ((value >> 0) & 0xff) / 255;

function getMatrix(rColor: number, gColor: number, bColor: number) {
	return `
		${r(rColor)} ${r(gColor)} ${r(bColor)} 0 0
		${g(rColor)} ${g(gColor)} ${g(bColor)} 0 0
		${b(rColor)} ${b(gColor)} ${b(bColor)} 0 0
		0 0 0 1 0
	`;
}

export const ColorFilterProvider = (props: { children: React.ReactNode }) => {
	const id = useUniqueId("color-filter-");

	return (
		<ColorFilterContext.Provider value={id}>
			<svg>
				{
					Color.List
						.map((color) => {
							const { primary, shadow } = getSpotColors(color);

							return (
								<filter id={`${id}-${color}`} key={color}>
									<feColorMatrix
										type="matrix"
										colorInterpolationFilters="sRGB"
										values={getMatrix(primary, VisorColor, shadow)}
									/>
								</filter>
							);
						})
				}
			</svg>
			{props.children}
		</ColorFilterContext.Provider>
	);
};

export const useColorFilter = (color: Color) => {
	const id = React.useContext(ColorFilterContext);

	if (id === undefined) {
		throw new Error("useColorFilter must be used within a ColorFilterProvider");
	}

	return `url(#${id}-${color})`;
};

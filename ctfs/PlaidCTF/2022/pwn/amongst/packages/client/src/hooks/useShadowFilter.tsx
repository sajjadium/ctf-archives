import React from "react";

import { useUniqueId } from "./useUniqueId";

const ShadowFilterContext = React.createContext<string | undefined>(undefined);

export const ShadowFilterProvider = (props: { children: React.ReactNode }) => {
	const id = useUniqueId("shadow-filter-");

	return (
		<ShadowFilterContext.Provider value={id}>
			<svg>
				<filter id={id}>
					<feColorMatrix
						type="matrix"
						colorInterpolationFilters="sRGB"
						values={`
							0.455 0     0     0 0
							0     0.420 0     0 0
							0     0     0.500 0 0
							0     0     0     1 0
						`}
					/>
				</filter>
			</svg>
			{props.children}
		</ShadowFilterContext.Provider>
	);
};

export const useShadowFilter = () => {
	const id = React.useContext(ShadowFilterContext);

	if (id === undefined) {
		throw new Error("useShadowFilter must be used within a ShadowFilterProvider");
	}

	return `url(#${id})`;
};

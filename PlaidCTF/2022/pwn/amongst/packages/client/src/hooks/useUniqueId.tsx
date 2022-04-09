import React from "react";

let nextId = 0;

export const useUniqueId = (prefix = "") => {
	const idRef = React.useRef<string | undefined>(undefined);

	if (idRef.current === undefined) {
		idRef.current = `${prefix}${nextId}`;
		nextId++;
	}

	return idRef.current;
};

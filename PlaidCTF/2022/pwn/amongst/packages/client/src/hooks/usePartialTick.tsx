import React from "react";

export const PartialTickContext = React.createContext<number>(0);
export const usePartialTick = () => React.useContext(PartialTickContext);

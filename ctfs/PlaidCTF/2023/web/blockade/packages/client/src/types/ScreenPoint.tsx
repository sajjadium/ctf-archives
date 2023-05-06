import { createPointLike } from "@puzzled/types";

export const ScreenPoint = createPointLike("ScreenPoint");
export type ScreenPoint = InstanceType<typeof ScreenPoint>;

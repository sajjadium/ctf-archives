import { createBrowserHistory } from "history";

export const History = createBrowserHistory();
export const navigate = (path: string) => History.push(path);
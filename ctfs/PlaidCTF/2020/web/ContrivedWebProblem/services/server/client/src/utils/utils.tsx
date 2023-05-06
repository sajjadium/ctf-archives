import { useHistory as useOGHistory } from "react-router";

export const unreachable = (t: never): never => t;
export const useHistory = () => {
    const history = useOGHistory();
    let push = history.push.bind(history);
    let newHistory = Object.assign(history, { push: ((path: string) => { setTimeout(() => push(path), 1) }) as any });
    return newHistory;
}

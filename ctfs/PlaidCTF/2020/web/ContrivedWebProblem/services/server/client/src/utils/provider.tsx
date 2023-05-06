import * as React from "react";

export const createProvider = <T extends unknown>(getData: () => Promise<T> | T) => {
    const Context = React.createContext<{ data: null | T, refresh: () => void }>({ data: null as T, refresh: () => { throw new Error("No provider")} });

    const Provider = (props: { children: React.ReactNode }) => {
        let [pending, setPending] = React.useState(false);
        let [data, setData] = React.useState<T>(null as T);

        let refresh = async () => {
            if (pending) {
                return;
            }

            setPending(true);
            let data = await getData()
            setData(data);
            setPending(false);
        };

        if (data === null && !pending) {
            refresh();
        }

        return (
            <Context.Provider value={{ data, refresh }}>
                { props.children }
            </Context.Provider>
        );
    }

    return { Provider, Context };
}
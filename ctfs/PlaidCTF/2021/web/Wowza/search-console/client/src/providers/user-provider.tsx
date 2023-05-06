import * as React from "react";

import { api } from "../client";
import { Loadable } from "../utils";

export const UserContext = React.createContext<{ user: Loadable<string>, refresh: () => void }>({ user: { loading: true }, refresh: () => {} });

export interface Props {
    children: React.ReactNode;
}

export const UserProvider = (props: Props) => {
    const [loading, setLoading] = React.useState(true);
    const [user, setUser] = React.useState<string | undefined>();

    const refresh = async () => {
        try {
            setLoading(true);
            const { username } = await api.user.self();
            setUser(username);
        } catch (e) {
            setUser(undefined);
        }
        setLoading(false);
    }

    React.useEffect(() => {
        refresh();

        return () => { setLoading(false) };
    }, []);

    return (
        <UserContext.Provider value={{ user: { value: user, loading }, refresh }}>
            { props.children }
        </UserContext.Provider>
    );
};

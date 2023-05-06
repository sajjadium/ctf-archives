import * as React from "react";

import { SiteClient } from "@wowza/search-console/client";

import { api } from "../client";
import { Loadable } from "../utils";

export const SiteContext = React.createContext<{ sites: Loadable<SiteClient.Site[]>, refresh: () => Promise<void> }>({ sites: { loading: true }, refresh: async () => {} });

export interface Props {
    children: React.ReactNode;
}

export const SiteProvider = (props: Props) => {
    const [loading, setLoading] = React.useState(true);
    const [sites, setSites] = React.useState<SiteClient.Site[] | undefined>();

    const refresh = async () => {
        try {
            setLoading(true);
            const sites = await api.site.sites();
            setSites(sites);
        } catch (e) {
            setSites(undefined);
        }
        setLoading(false);
    }

    React.useEffect(() => {
        refresh();

        return () => { setLoading(false) };
    }, []);

    return (
        <SiteContext.Provider value={{ sites: { value: sites, loading }, refresh }}>
            { props.children }
        </SiteContext.Provider>
    );
};

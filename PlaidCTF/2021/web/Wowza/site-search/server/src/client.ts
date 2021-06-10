import fetch from "node-fetch";

import { getBody } from "./utils";

const consoleUrl = process.env.CONSOLE_URL ?? "http://localhost:6284/";

export interface Result {
    name: string;
    path: string;
    description: string;
    isStale: boolean;
}

const cache: { [domain: string]: { [query: string]: Result[] } } = { };

export const getResults = async (domain: string, query: string) => {
    if (cache[domain]?.[query]) {
        return cache[domain][query];
    }

    const tokens = query
        .split(/\s+/g)
        .map((x) => x.replace(/[^a-zA-Z0-9]+/g, ""))
        .filter((x) => x !== "");

    const results = await fetch(new URL("/search", consoleUrl), {
        headers: {
            "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({ domain, query: tokens }),
    });

    const searchResults: Result[] = await results.json();
    const patched = await Promise.all(
        searchResults
            .map(async (result) => {
                if (result.isStale) {
                    const pageUrl = new URL(result.path, "http://" + domain);
                    try {
                        const refetch = await fetch(pageUrl);
                        const body = await refetch.text();
                        result.description = getBody(body).join(" ").trim();
                    } catch (e) {
                        // pass
                    }
                }

                return result;
            })
    );

    const domainCache = cache[domain] ?? {};
    domainCache[query] = patched;
    cache[domain] = domainCache;

    return patched;
}
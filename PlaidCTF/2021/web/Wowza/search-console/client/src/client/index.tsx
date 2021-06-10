import { Client, Fetcher } from "@wowza/search-console/client";

const fetcher: Fetcher = {
    async get(url) {
        try {
            const result = await fetch(url, {
                credentials: "include",
            });
            const json = await result.json();
            if (!result.ok) {
                throw (json as { "error": string })["error"];
            }
            return json
        } catch (e) {
            throw e;
        }
    },

    async post(url, body) {
        try {
            const result = await fetch(url, {
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body),
                method: "POST",
            });
            const json = await result.json();
            if (!result.ok) {
                throw (json as { "error": string })["error"];
            }
            return json;
        } catch (e) {
            throw e;
        }
    }
}

export const api = new Client(fetcher);
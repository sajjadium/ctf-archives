export const rest = async (endpoint: string, query: [string, string][] = [], body: object | undefined= undefined) => {
    let search = query.map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join("&");
    let req = await fetch(`/api/${endpoint}?${search}`, {
        method: body === undefined ? "GET" : "POST",
        credentials: "include",
        body: body === undefined ? undefined : JSON.stringify(body),
        headers: {
            "Content-Type": "application/json",
        },
    });

    return [req.status, await req.text()] as const;
}
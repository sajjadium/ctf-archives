class Options {
    method: string;
    credentials: string;
    headers: object;
    body: string;
}

export default async function api(method, route, data={}, cookies="", ssr=false) {
    var options = new Options();
    var url = `${process.env.NEXT_PUBLIC_BACKEND}${route}`;
    options.credentials = "include";
    options.method = method;
    options.headers = {};

    if (ssr) {
        options.headers["Cookie"] = cookies;
        var url = `http://backend:3000${route}`;
    }

    if (Object.keys(data).length !== 0) {
        options.headers["Content-Type"]  = "application/json";
        options.body = JSON.stringify(data);
    }

    var res = await fetch(url, (options as RequestInit));
    return res.json();
}
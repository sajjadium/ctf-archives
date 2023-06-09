import {Request, ResponseObject, ResponseToolkit} from "@hapi/hapi";
import {base64decode, ipToCountryCode} from "./utils";
import {readFileSync} from "fs";
import Path from "path";
import {fileURLToPath} from "url";

const template: string = readFileSync(Path.join(Path.dirname(fileURLToPath(import.meta.url)), '../static/index.html')).toString()

export async function index(request: Request, h: ResponseToolkit): Promise<ResponseObject> {
return h.response(template.replace('@FOOTER@', `Generated: ${Date.now()} - Request origin: ${await ipToCountryCode(request.app.realIp)}`))
    .type('text/html')
}

// Protect the users privacy by proxying 3rd-party requests through our own backend
export async function proxyRequest(request: Request, h: ResponseToolkit): Promise<ResponseObject> {
    const url: string = base64decode(request.params.endpoint)

    console.log('proxy_request', url)

    if (!url.startsWith('https://')) {
        return h.response('invalid url')
            .code(401);
    }

    const resp = await fetch(url)

    return h.response(new Buffer(await resp.arrayBuffer()))
        .type(resp.headers.get('content-type') || 'text/plain')
}

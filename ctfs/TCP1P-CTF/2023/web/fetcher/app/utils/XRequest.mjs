import https from "https";
import http from "http"
import { ProxyAgent } from "proxy-agent";


export class XRequest {
    constructor(opts) {
        Object.assign(this, opts);
    }

    getProxy() {
        return new ProxyAgent({ getProxyForUrl: () => this.proxyUrl });
    }
    get(url) {
        return new Promise((resolve, reject) => {
            var path;
            if (this.baseUrl) {
                path = this.baseUrl + url
            } else {
                path = url
            }
            https.get(path, { agent: this.getProxy() }, resp => {
                let data = ""
                resp.on("data", chunk => data += chunk)
                resp.on("end", () => resolve(data))
                resp.on("error", reject)
            })

        });
    }
    listen(app, port) {
        return http.createServer(app).listen(port, () => {
            console.log(`listening @ http://localhost:${port}`)
        })
    }
}

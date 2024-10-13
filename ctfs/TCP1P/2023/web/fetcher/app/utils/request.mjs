import { XRequest } from "./XRequest.mjs"


async function get(url, opts) {
    const request = new XRequest({ ...opts })
    return await request.get(url)
}

function listen(app, port, opts) {
    const request = new XRequest({ ...opts })
    return request.listen(app, port)
}

export { get, listen }

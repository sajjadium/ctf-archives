import {Request, ResponseToolkit} from "@hapi/hapi";

declare module "@hapi/hapi" {
    interface RequestApplicationState {
        realIp: string
    }
}

export function checkIpHeader(request: Request, h: ResponseToolkit) {
    request.app.realIp = request.headers['cf-connecting-ip'] || request.info.remoteAddress

    return h.continue
}

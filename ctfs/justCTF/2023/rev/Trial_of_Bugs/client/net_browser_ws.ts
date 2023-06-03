import {NetImplBase} from "../share/net/net_impl_base";
import {DisconnectInfo, DisconnectSource} from "../share/net/net_interface";

export class NetBrowserWs extends NetImplBase {
    ws: WebSocket;
    client = true;

    private closed: boolean = false;

    constructor(ws: WebSocket) {
        super();
        this.ws = ws;
        ws.onmessage = (ev) => {
            if (this.closed)
                return;
            this.onReceiveRaw(ev.data as any);
        };
        ws.onclose = () => this.disconnect({source: DisconnectSource.SOCKET_DISCONNECT});
    }

    protected sendRaw(data: string): void {
        if (!this.closed)
            this.ws.send(data);
    }

    disconnect(info: DisconnectInfo) {
        this.closed = true;
        this.ws.close();
        super.disconnect(info);
    }

    toString() {
        return this.ws.url;
    }
}

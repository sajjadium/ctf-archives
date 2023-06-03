import {DisconnectInfo, DisconnectSource, NetInterface} from "./net_interface";
import {Rpc} from "./rpc";
import {ID_PING, ID_PONG} from "./packet_ids";

export interface Backpressure {
    cancelPending(): void;
    check(packetId: number, packetData: any): boolean;
    enqueue(cb: () => void): void;
}

export abstract class NetImplBase implements NetInterface {
    private handlers: {[packetId: number]: (data: any) => void} = {};
    private disconnectHandlers: ((info: DisconnectInfo) => void)[] = [];
    rpc: Rpc;
    backpressure?: Backpressure;
    abstract client: boolean;
    disconnected: boolean = false;
    schemaValidationCallback?: (data: any) => void;

    protected constructor() {
        this.rpc = new Rpc(this);

        this.addPacketHandler(ID_PING, (data: any) => this.send(ID_PONG, parseInt(data)));
    }

    addPacketHandler(packetId: number, handler: (data: any) => void): any {
        this.handlers[packetId] = handler;
    }

    addDisconnectHandler(handler: (info: DisconnectInfo) => void) {
        this.disconnectHandlers.push(handler);
    }

    send(packetId: number, data: any): void {
        this.sendRaw(JSON.stringify([packetId, data]));
    }

    protected onReceiveRaw(data: string) {
        if (this.disconnected)
            return;

        try {
            const parsed = JSON.parse(data);
            if (this.schemaValidationCallback)
                this.schemaValidationCallback(parsed);
            if (!Array.isArray(parsed) || parsed.length !== 2)
                throw new Error("bad data");

            if (this.backpressure && !this.backpressure.check(parsed[0], parsed[1])) {
                this.enqueueToBackpressure(parsed);
            } else {
                this.handlers[parsed[0]](parsed[1]);
            }
        } catch (e) {
            console.error(e);
            this.disconnect({
                source: DisconnectSource.HANDLE_ERROR,
                handleError: e || new Error()
            });
        }
    }

    private enqueueToBackpressure(parsed: any) {
        this.backpressure!.enqueue(() => {
            try {
                this.handlers[parsed[0]](parsed[1]);
            } catch (e) {
                console.error(e);
                this.disconnect({
                    source: DisconnectSource.HANDLE_ERROR,
                    handleError: e || new Error()
                });
            }
        });
    }

    protected abstract sendRaw(data: string): void;

    disconnect(info: DisconnectInfo): void {
        if (this.disconnected)
            return;

        this.disconnected = true;
        this.backpressure?.cancelPending();
        for (const handler of this.disconnectHandlers)
            handler(info);
    }
}

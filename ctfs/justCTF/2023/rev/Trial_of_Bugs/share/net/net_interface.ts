import {Rpc} from "./rpc";

export enum DisconnectSource {
    SOCKET_DISCONNECT,
    TIMEOUT,
    SESSION_SERVER_REQUEST,
    HANDLE_ERROR,
    USER_REQUEST
}
export type DisconnectInfo = {
    source: DisconnectSource,
    handleError?: any|undefined;
}

export interface NetInterface {
    client: boolean;
    rpc: Rpc;
    disconnected: boolean;
    ip?: string;

    addPacketHandler(packetId: number, handler: (data: any) => void): any;

    addDisconnectHandler(handler: (info: DisconnectInfo) => void): void;

    send(packetId: number, data: any): void;

    disconnect(info: DisconnectInfo): void;
}

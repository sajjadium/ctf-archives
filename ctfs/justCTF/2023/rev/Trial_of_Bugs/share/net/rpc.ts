import {NetInterface} from "./net_interface";
import {
    ID_RPC_QUEUE_EXECUTE_DONE,
    ID_RPC_QUEUE_EXECUTE_REQUEST,
    ID_RPC_SHARED_EXECUTE
} from "./packet_ids";
import {Queue} from "../util/queue";

export class RpcSingleton {
    net: NetInterface;

    constructor(net: NetInterface) {
        this.net = net;
        net.rpc.addSingleton(this);
    }
}

type SyncFnInfo = {
    singletonName: string,
    target: any
}

const BLOCK_SHARED = 0;
const BLOCK_PRIVATE = 1;

export class Rpc {
    public static serverSyncFns: {[name: string]: SyncFnInfo} = {};
    public static clientSyncFns: {[name: string]: SyncFnInfo} = {};

    private net: NetInterface;
    private blockStack: number[] = [];
    private singletons: {[objectType: string]: RpcSingleton} = {};
    private remoteExecQueue = new Queue<() => void>();

    constructor(net: NetInterface) {
        this.net = net;
        net.addPacketHandler(ID_RPC_SHARED_EXECUTE, this._doRemoteRpc.bind(this));
        net.addPacketHandler(ID_RPC_QUEUE_EXECUTE_REQUEST, (data) => {
            this._doRemoteRpc(data);
            net.send(ID_RPC_QUEUE_EXECUTE_DONE, null);
        });
        net.addPacketHandler(ID_RPC_QUEUE_EXECUTE_DONE, () => {
            const item = this.remoteExecQueue.pop();
            item!();
        });
        this.blockStack.push(BLOCK_PRIVATE);
    }

    private _doRemoteRpc(data: any) {
        const fnInfo = this.net.client ? Rpc.clientSyncFns[data[0]] : Rpc.serverSyncFns[data[0]];
        if (!fnInfo)
            throw new Error("Function not found for RPC: " + data[0]);
        const self = this.singletons[fnInfo.singletonName];
        if (!self)
            throw new Error("Singleton not found: " + fnInfo.singletonName + " (for RPC: " + data[0] + ")");
        this.enterSharedBlock();
        fnInfo.target.call(self, ...data.slice(1));
        this.exitSharedBlock();
    }

    get hasPendingSharedExecutions() {
        return this.remoteExecQueue.peek() !== null;
    }

    flushPendingSharedExecutions() {
        if (!this.net.disconnected)
            throw new Error('Can only flush pending shared executions on disconnect');
        while (this.remoteExecQueue.peek() !== null) {
            const el = this.remoteExecQueue.pop()!;
            el();
        }
    }

    get inSharedBlock() {
        return this.blockStack[this.blockStack.length - 1] === BLOCK_SHARED;
    }

    enterSharedBlock() {
        this.blockStack.push(BLOCK_SHARED);
    }

    exitSharedBlock() {
        this.blockStack.pop();
    }

    enterPrivateBlock() {
        this.blockStack.push(BLOCK_PRIVATE);
    }

    exitPrivateBlock() {
        this.blockStack.pop();
    }

    runPrivate(cb: () => void) {
        this.enterPrivateBlock();
        try {
            cb();
        } finally {
            this.exitPrivateBlock();
        }
    }

    runServerOnly(cb: () => void) {
        if (!this.net.client)
            this.runPrivate(cb);
    }

    onSharedExecute(name: string, ...args: any) {
        if (!this.inSharedBlock)
            this.net.send(ID_RPC_SHARED_EXECUTE, [name, ...args]);
    }

    requestRemoteExecute(name: string, cb: () => void, ...args: any) {
        this.remoteExecQueue.push(cb);
        this.net.send(ID_RPC_QUEUE_EXECUTE_REQUEST, [name, ...args]);
    }

    addSingleton(singleton: RpcSingleton) {
        this.singletons[singleton.constructor.name] = singleton;
    }

}

export function bothExecute(opts: {clientInvokable?: boolean, clientSync?: boolean}) {
    return (target: RpcSingleton, propertyKey: string, descriptor: PropertyDescriptor) => {
        const name = target.constructor.name + '.' + propertyKey;

        const orig = descriptor.value;
        const fnInfo: SyncFnInfo = {
            singletonName: target.constructor.name,
            target: orig
        };
        Rpc.clientSyncFns[name] = fnInfo;
        if (opts.clientInvokable)
            Rpc.serverSyncFns[name] = fnInfo;


        descriptor.value = function (...args: any): any {
            const rpc = (this as any).net.rpc;
            rpc.onSharedExecute(name, ...args);
            rpc.enterSharedBlock();
            orig.call(this, ...args);
            rpc.exitSharedBlock();
        };
        if (opts.clientSync) {
            const mainInvoker = descriptor.value;
            descriptor.value = function (...args: any): any {
                if ((this as any).net.client || (this as any).net.rpc.inSharedBlock) {
                    return mainInvoker.call(this, ...args);
                } else {
                    (this as any).net.rpc.requestRemoteExecute(name, () => {
                        const rpc = (this as any).net.rpc;
                        rpc.enterSharedBlock();
                        orig.call(this, ...args);
                        rpc.exitSharedBlock();
                    }, ...args);
                }
            };
        }
    };
}

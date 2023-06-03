import {NetInterface} from "./net_interface";

const ID_START_SHARED = 0;
const ID_START_SERVER = 1000000000;
const ID_START_CLIENT = 2000000000;

export class NetIdCounter {
    private readonly net: NetInterface;
    private sharedCounter: number = ID_START_SHARED;
    private localCounter: number|null;
    
    constructor(net: NetInterface, allowClientId: boolean = false) {
        this.net = net;
        this.localCounter = net.client ? ID_START_CLIENT : ID_START_SERVER;
        if (!allowClientId)
            this.localCounter = null;
    }
    
    next() {
        if (this.net.rpc.inSharedBlock)
            return this.sharedCounter++;
        return this.localCounter!++;
    }
}

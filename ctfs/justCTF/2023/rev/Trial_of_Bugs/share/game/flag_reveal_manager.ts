import {bothExecute, RpcSingleton} from "../net/rpc";
import {NetInterface} from "../net/net_interface";
import {GameGlobalKVManager} from "./game_global_kv_manager";

export class FlagRevealManager extends RpcSingleton {
    kv: GameGlobalKVManager;

    constructor(net: NetInterface, kv: GameGlobalKVManager) {
        super(net);
        this.kv = kv;
    }

    reveal(varName: string, envName: string) {
        this.net.rpc.runServerOnly(() => {
            const varValue = process.env['FLAG_' + envName]?.toString() || '';
            this.setFlag(varName, varValue);
        });
    }

    @bothExecute({clientSync: true})
    private setFlag(varName: string, varValue: string) {
        this.kv.set(varName, varValue);
    }
}

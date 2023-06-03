import {bothExecute, RpcSingleton} from "../net/rpc";
import {Player} from "./player";
import {ID_RPC_QUEUE_EXECUTE_DONE, ID_RPC_QUEUE_EXECUTE_REQUEST, ID_RPC_SHARED_EXECUTE} from "../net/packet_ids";
import {CollisionSystem} from "../collision/collision_system";

export class Debug extends RpcSingleton {
    private player: Player;

    constructor(player: Player) {
        super(player.net);
        this.player = player;
    }

    @bothExecute({clientInvokable: true})
    dumpWorld() {
        this.net.rpc.runServerOnly(() => {
            console.log(JSON.parse(JSON.stringify(this.player.map.currentWorld!.world.save())));
        })
    }

    @bothExecute({clientInvokable: true})
    saveGame() {
        this.net.rpc.runServerOnly(() => {
            this.player.persistence!.saveGame();
        })
    }

    @bothExecute({clientInvokable: true})
    setEnforceTickRate(enabled: boolean) {
        this.player.map.enforceTickRate = enabled;
    }

    @bothExecute({clientInvokable: true})
    tp(pointName: string) {
        this.net.rpc.runServerOnly(() => {
            this.player.map.requestEnterByPoint(this.player.map.currentWorldName, this.player.map.currentWorld.loader.mapMeta.name, pointName);
        });
    }

    @bothExecute({clientInvokable: true})
    reportMetrics() {
        this.net.rpc.runServerOnly(() => {
            this.reportMetricsResponse({
                'worldCount': Object.keys(this.player.map.worlds).length,
                'entityCount': Object.keys(this.player.map.currentWorld.world.entities).length,
                'collisionBodyCount': this.player.map.currentWorld.world.getSingleton(CollisionSystem)?.system.all().length
            });
        })
    }

    @bothExecute({clientSync: true})
    reportMetricsResponse(metrics: any) {
        if (this.net.client)
            console.log(metrics);
    }

    sendInvalidPacket() {
        this.net.send(1234, null);
        this.net.send(ID_RPC_SHARED_EXECUTE, null);
        this.net.send(ID_RPC_QUEUE_EXECUTE_REQUEST, null);
        this.net.send(ID_RPC_QUEUE_EXECUTE_DONE, null);
    }

}

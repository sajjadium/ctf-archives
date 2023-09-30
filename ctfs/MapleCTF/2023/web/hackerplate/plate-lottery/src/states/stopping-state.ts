import { WebSocket } from "ws";
import { STOPPING_LENGTH, STOPPING_TICK_INTERVAL, TOTAL_TICKS } from '../util/constants.js';
import { PlayerMessage } from '../util/types.js';
import ChoosingState from './choosing-state.js';
import PlayerContext from './player-context.js';
import PlayerState from './player-state.js';

export default class StoppingState extends PlayerState {
    lastTick: number;
    constructor(context: PlayerContext, ws: WebSocket, vin: string, plateSpaceSize: number, lastTick: number) {
        super(context, ws, vin, plateSpaceSize);
        this.lastTick = lastTick;
        this.currentTick = 0;
        this.plates = [];
    }

    nextTick() {
        this.currentTick++;
        if (this.currentTick >= STOPPING_LENGTH * STOPPING_TICK_INTERVAL) {
            this.plates = this.context.seededRandomSequence[TOTAL_TICKS - this.lastTick - 1 + Math.floor(this.currentTick / STOPPING_TICK_INTERVAL)];
            this.context.changeState(new ChoosingState(this.context, this.ws, this.vin, this.plateSpaceSize, this.plates));;
        } else if (this.currentTick % STOPPING_TICK_INTERVAL === 0) {
            this.plates = this.context.seededRandomSequence[TOTAL_TICKS - this.lastTick - 1 + Math.floor(this.currentTick / STOPPING_TICK_INTERVAL)];
            const response = {
                "action": "stopping",
                "state": this.plates,
                "time": this.currentTick
            }
            this.ws.send(JSON.stringify(response));
        }
    }

    handleMessage(mesg: PlayerMessage) {
        switch (mesg.action) {
            default:
                this.ws.send(JSON.stringify({
                    "action": "error",
                    "message": "currently stopping"
                }));
                break;
        }
    }
}
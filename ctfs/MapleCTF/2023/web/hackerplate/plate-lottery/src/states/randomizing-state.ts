import { WebSocket } from 'ws';
import PlayerState from './player-state.js';
import PlayerContext from './player-context.js';
import StoppingState from './stopping-state.js';
import { PlayerMessage } from '../util/types.js';
import { TOTAL_TICKS } from '../util/constants.js';

export default class RandomizingState extends PlayerState {
    constructor(context: PlayerContext, ws: WebSocket, vin: string, plateSpaceSize: number) {
        super(context, ws, vin, plateSpaceSize);
    }

    nextTick() {
        if (this.currentTick <= this.tickToStop) {
            this.context.changeState(new StoppingState(this.context, this.ws, this.vin, this.plateSpaceSize, this.currentTick));
        } else {
            this.currentTick--;
            this.plates = this.context.seededRandomSequence[TOTAL_TICKS - this.currentTick + 1];
            const response = {
                "action": "randomizing",
                "state": this.plates,
                "time": this.currentTick
            }
            this.ws.send(JSON.stringify(response));
        }
    }

    handleMessage(mesg: PlayerMessage) {
        switch (mesg.action) {
            case 'stop':
                const tickToStop = parseInt(mesg.tickToStop ?? "0", 10);
                if (tickToStop < 0) {
                    this.ws.send(JSON.stringify({
                        "action": "error",
                        "message": "invalid tick to stop at"
                    }));
                } else {
                    this.tickToStop = tickToStop;
                    this.ws.send(JSON.stringify({
                        action: 'notify',
                        message: `stopping at tick ${tickToStop}...`,
                    }));
                }
                break;
            default:
                this.ws.send(JSON.stringify({
                    "action": "error",
                    "message": "action not applicable"
                }));
                break;
        }
    }
}
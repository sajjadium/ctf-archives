import { WebSocket } from "ws";
import { PlayerMessage } from '../util/types.js';
import PlayerContext from './player-context.js';
import PlayerState from './player-state.js';

export default class TerminatedState extends PlayerState {
    constructor(context: PlayerContext, ws: WebSocket, vin: string) {
        super(context, ws, vin, 0);
    }

    nextTick() {
        // do nothing, waiting to get cleaned up by the context
    }

    handleMessage(mesg: PlayerMessage) {
        switch (mesg.action) {
            default:
                this.ws.send(JSON.stringify({
                    "action": "error",
                    "message": "process already complete"
                }))
                break;
        }
    }
}
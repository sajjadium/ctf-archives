import { WebSocket } from "ws";
import { PlayerMessage } from '../util/types.js';
import PlayerState from './player-state.js';
import { NUM_PLATES, TOTAL_TICKS, STOPPING_LENGTH, SECRET, INTERNAL_SERVER } from '../util/constants.js';
import { makeRequest, randomIndices } from '../util/util.js';
import InitialState from "./initial-state.js";
import TerminatedState from "./terminated-state.js";

export default class PlayerContext {
    // the class that contains this attempt's state machine
    state: PlayerState;
    platesToIgnore: number[];
    platePossibilitySpace: number[];
    seededRandomSequence: number[][];
    constructor(ws: WebSocket, message: string) {
        try {
            const {action, vin, ...rest} = JSON.parse(message);
            if (action != "init") {
                throw new Error("action is not init");
            }
            this.state = new InitialState(this, ws, vin);
        } catch (e) {
            throw new Error("cannot parse message, or action is not init");
        }
    }
    nextTick() {
        this.state.nextTick();
    }
    handleMessage(message: string) {
        try {
            const mesg: PlayerMessage = JSON.parse(message);
            this.state.handleMessage(mesg);
        } catch (e) {
            this.state.ws.send(JSON.stringify({
                "action": "error",
                "message": e.message
            }))
        }
    }
    changeState(state: PlayerState) {
        this.state = state;
    }
    isConnectionClosed() {
        if (this.state instanceof TerminatedState) {
            this.state.ws.close();
        }
        return this.state.ws.readyState == this.state.ws.CLOSED;
    }
    async earlyTerminate() {
        this.changeState(new TerminatedState(this.state.context, this.state.ws, this.state.vin));
        try {
            await makeRequest(`${INTERNAL_SERVER}/lottery/cancel`, "POST", {
                "vin": this.state.vin,
                "secret": SECRET
            });
        } catch (e) {}
    }
}
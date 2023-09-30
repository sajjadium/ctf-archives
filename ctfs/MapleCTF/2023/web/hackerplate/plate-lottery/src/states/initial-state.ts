import { WebSocket } from "ws";
import PlayerContext from './player-context.js';
import PlayerState from './player-state.js';
import { PlayerMessage } from '../util/types.js';
import RandomizingState from "./randomizing-state.js";
import { getPlatePossibilitySpace, makeRequest, randomIndices } from "../util/util.js";
import { INTERNAL_SERVER, NUM_PLATES, SECRET, STOPPING_LENGTH, TOTAL_TICKS } from "../util/constants.js";
import TerminatedState from "./terminated-state.js";

export default class InitialState extends PlayerState {
    isReady: boolean;
    constructor(context: PlayerContext, ws: WebSocket, vin: string) {
        super(context, ws, vin, -1);
        this.startReadying()
    }

    async startReadying() {
        try {
            const res = await makeRequest(`${INTERNAL_SERVER}/lottery/attempt?secret=${SECRET}&vin=${this.vin}`, "GET", {});
            const { plates, ...rest } = JSON.parse(res);
            // const plates = []; // offline debug
            this.context.platesToIgnore = plates;
            this.context.platePossibilitySpace = getPlatePossibilitySpace(plates);
            this.context.seededRandomSequence = [];
            for (let i = 0; i < (TOTAL_TICKS + STOPPING_LENGTH); i++) {
                this.context.seededRandomSequence.push(randomIndices(this.context.platePossibilitySpace.length, NUM_PLATES));
            }
            this.ws.send(JSON.stringify({
                "action": "ready",
                "state": plates,
            }));
            this.isReady = true;
        } catch (e) {
            this.ws.send(JSON.stringify({
                "action": "error",
                "message": e
            }));
            console.log(e);
            this.context.changeState(new TerminatedState(this.context, this.ws, this.vin));
        }
    }

    nextTick() {
        // do nothing until we get instructions to start randomizing
    }

    handleMessage(mesg: PlayerMessage) {
        switch (mesg.action) {
            case 'randomize':
                if (this.isReady) {
                    this.context.changeState(new RandomizingState(this.context, this.ws, this.vin, this.plateSpaceSize));
                } else {
                    this.ws.send(JSON.stringify({
                        "action": "error",
                        "message": "not ready"
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
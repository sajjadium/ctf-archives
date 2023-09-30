import { WebSocket } from "ws";
import PlayerContext from './player-context.js';
import PlayerState from './player-state.js';
import { CHOOSING_TICKS, INTERNAL_SERVER, SECRET } from '../util/constants.js';
import { PlayerMessage } from '../util/types.js';
import TerminatedState from './terminated-state.js';
import { findPlateFromIndex, makeRequest } from "../util/util.js";

const FLAG = process.env.FLAG || "maple{test_flag}";

export default class ChoosingState extends PlayerState {
    constructor(context: PlayerContext, ws: WebSocket, vin: string, plateSpaceSize: number, finalPlateIndices: number[]) {
        super(context, ws, vin, plateSpaceSize);
        this.currentTick = CHOOSING_TICKS;
        this.plates = finalPlateIndices;
        this.currentChoice = 0; // pick first plate by default if time runs out
        const response = {
            "action": "choosing",
            "state": this.plates,
            "time": this.currentTick
        }
        this.ws.send(JSON.stringify(response));
    }

    nextTick() {
        this.currentTick--;
        if (this.currentTick <= 0) {
            this.confirmChoice(this.plates, this.currentChoice);
            this.context.changeState(new TerminatedState(this.context, this.ws, this.vin));
        } else {
            const response = {
                "action": "choosing",
                "time": this.currentTick,
            }
            this.ws.send(JSON.stringify(response));
        }
    }

    async handleMessage(mesg: PlayerMessage) {
        switch (mesg.action) {
            case 'choose':
                this.currentChoice = parseInt(mesg.plate ?? "-1", 10);
                this.ws.send(JSON.stringify({
                    "action": "notify",
                    "message": "choice received"
                }));
                break;
            case 'confirm':
                const isLeet = await this.confirmChoice(this.plates, this.currentChoice);
                this.ws.send(JSON.stringify({
                    "action": "notify",
                    "message": "choice confirmed",
                    "flag": isLeet ? FLAG : "",
                }));
                this.context.changeState(new TerminatedState(this.context, this.ws, this.vin));
                break;
            default:
                this.ws.send(JSON.stringify({
                    "action": "error",
                    "message": "action not applicable"
                }));
                break;
        }
    }

    async confirmChoice(plates: number[], choice: number): Promise<boolean> {
        try {
            const plateIndex = Math.floor(plates[choice]); // like 10001 == plates[0]
            const plate = findPlateFromIndex(plateIndex, this.context.platesToIgnore);
            console.log("vin at confirmChoice is " + this.vin);
            const res = await makeRequest(`${INTERNAL_SERVER}/lottery/complete`, "POST", {
                secret: SECRET,
                vin: this.vin,
                plate: this.context.platePossibilitySpace[Math.floor(plates[choice])],
            });
            if (plate === "L-337-HX") {
                return true;
            }
        } catch (e) {
            console.log(e)
        }
        return false;
    }
}
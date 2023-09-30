import { WebSocket } from "ws";
import { TOTAL_TICKS } from '../util/constants.js';
import { PlayerMessage } from '../util/types.js';
import PlayerContext from './player-context.js';

export default abstract class PlayerState {
    context: PlayerContext; // the context this state is associated with
    ws: WebSocket; // User's websocket connection
    plates: number[]; // an array of plate indices
    ticksUntilStop: number; // tracks how many ticks until randomization ends
    currentTick: number; // tracks how many ticks have passed
    // we're running our plate selection terminals on decades-old hardware
    // like, really old
    // so we let terminals send a specific tick to stop randomization at
    tickToStop: number; // records terminal input to stop randomization
    currentChoice: number; // the index of the plate the user chose
    vin: string; // the VIN of the vehicle to associate this plate with
    plateSpaceSize: number; // number of plates out of which we can choose

    constructor (context: PlayerContext, ws: WebSocket, vin: string, plateSpaceSize: number) {
        this.context = context;
        this.ws = ws;
        this.ticksUntilStop = 0;
        this.plates = [];
        this.currentTick = TOTAL_TICKS;
        this.tickToStop = 0; // by default, if time runs out we pick final iteration
        this.currentChoice = 0; // by default, just pick first plate
        this.vin = vin;
        this.plateSpaceSize = plateSpaceSize;
    }

    abstract nextTick(): void;
    abstract handleMessage(message: PlayerMessage): void;
}

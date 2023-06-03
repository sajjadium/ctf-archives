import {GameKey} from "./game_keys";

export class InputDevice {
    pressed: boolean[];

    constructor() {
        this.pressed = new Array(GameKey.Max).fill(false);
    }
}

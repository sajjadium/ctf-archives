import {InputDevice} from "./input_device";
import {bothExecute, RpcSingleton} from "../net/rpc";
import {NetInterface} from "../net/net_interface";
import {GameKey} from "./game_keys";

export class InputManager extends RpcSingleton {
    primary: InputDevice;

    constructor(net: NetInterface) {
        super(net);
        this.primary = new InputDevice();
    }

    @bothExecute({clientSync: true, clientInvokable: true})
    setKey(deviceId: number, key: GameKey, pressed: boolean) {
        this.primary.pressed[key] = pressed;
    }
}

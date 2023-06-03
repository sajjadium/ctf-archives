import {DisconnectSource, NetInterface} from "../share/net/net_interface";
import {ID_LOGIN_ERROR, ID_LOGIN_REQUEST, ID_LOGIN_RESPONSE, ID_LOGIN_WHITELIST_KEY} from "../share/net/packet_ids";
import {GameData} from "../share/game/game_data";
import {Player} from "../share/game/player";
import {ObservableField} from "../share/util/observable_field";

export class Connection {
    data: GameData;
    net: NetInterface;
    player: Player|null = null;
    connectState = new ObservableField<string>('connecting');
    disconnected = new ObservableField<boolean>(false);
    loginError: string|null = null;

    constructor(data: GameData, net: NetInterface) {
        this.data = data;
        this.net = net;

        net.addDisconnectHandler(() => this.disconnected.set(true));

        net.addPacketHandler(ID_LOGIN_RESPONSE, (data) => {
            console.log('logged in!');
            this.createPlayer(data);
        });
        net.addPacketHandler(ID_LOGIN_ERROR, (data) => {
            this.loginError = data;
            this.connectState.set('login_error');
            net.disconnect({source: DisconnectSource.USER_REQUEST});
        });
        if (data.config.serverKey)
            net.send(ID_LOGIN_WHITELIST_KEY, data.config.serverKey);
        net.send(ID_LOGIN_REQUEST, localStorage.token || null);
    }

    createPlayer(data: any) {
        if (data.token)
            localStorage.token = data.token;
        this.player = new Player(this.data, this.net);
        this.player.onEnterGame(data.playerData);
        this.connectState.set('connected');
    }
}

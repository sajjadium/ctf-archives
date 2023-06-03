import {GameLoader} from "./game_loader";
import {ObservableField} from "../share/util/observable_field";
import {GameData} from "../share/game/game_data";
import {NetBrowserWs} from "./net_browser_ws";
import {Connection} from "./connection";
import {GameMapRenderer} from "./render/game_map_renderer";
import {KEY_MAP} from "./key_map";
import "./game.css";
import {LOGIN_ERROR_PLAYER_LIMIT} from "../share/net/login_errors";

export class Client {
    loader: GameLoader = new GameLoader();
    loadComplete = new ObservableField<boolean>(false);
    connectError = new ObservableField<boolean>(false);
    connection = new ObservableField<Connection|null>(null);
    renderer: GameMapRenderer|null = null;

    start() {
        this.loader.loadAssets(() => this.onLoaded());

        window.addEventListener('keydown', (e) => {
            const connection = this.connection.get();
            if (e.key in KEY_MAP)
                connection?.player?.input.setKey(0, KEY_MAP[e.key], true);
        }, true);
        window.addEventListener('keyup', (e) => {
            const connection = this.connection.get();
            if (e.key in KEY_MAP)
                connection?.player?.input.setKey(0, KEY_MAP[e.key], false);
        }, true);
    }

    private onLoaded() {
        console.log('game data loaded');
        this.loadComplete.set(true);

        const data = new GameData(this.loader.config!, this.loader.scriptBlob!, this.loader.scriptComponentMeta!, this.loader.questMeta!, this.loader.tilesets!);

        const urls = typeof this.loader.config!.wsUrl === 'string' ? [this.loader.config!.wsUrl] : this.loader.config!.wsUrl;
        this.tryConnect(data, urls);
    }

    private tryConnect(data: GameData, urls: string[]) {
        const urlNo = Math.floor(Math.random() * urls.length);
        const url = urls[urlNo];

        let open = false;
        const socket = new WebSocket(url.replace('[host]', window.location.hostname));
        socket.onopen = e => {
            open = true;
            console.log('ws open');

            const net = new NetBrowserWs(socket);
            this.connection.set(new Connection(data, net));

            this.connection.get()!.connectState.addCallback(state => {
                if (state === 'connected') {
                    this.onConnected();
                } else if (state === 'login_error' && this.connection.get()!.loginError === LOGIN_ERROR_PLAYER_LIMIT && urls.length > 1) {
                    console.log('Player limit, trying another server');
                    this.connection.set(null);

                    socket.close();
                    open = false;
                    const newUrls = [...urls];
                    newUrls.splice(urlNo, 1);
                    this.tryConnect(data, newUrls);
                }
            });
        };
        socket.onerror = () => {
            if (!open) {
                this.connectError.set(true);
            }
        };
    }

    private onConnected() {
        const connection = this.connection.get()!;
        (window as any).debug = connection.player!.debug;

        const canvas = document.getElementById('canvas')! as HTMLCanvasElement;
        this.renderer = new GameMapRenderer(canvas.getContext('webgl', {premultipliedAlpha: false}) as WebGLRenderingContext, connection.player!);
    }
}

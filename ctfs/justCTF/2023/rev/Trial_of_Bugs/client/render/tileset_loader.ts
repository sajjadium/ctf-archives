import {DownloadGroup} from "../download_group";
import {Player} from "../../share/game/player";

export class TilesetLoader {
    readonly player: Player;
    private readonly loadTilesetGroups: {[name: string]: DownloadGroup} = {};
    tilesetImages: {[name: string]: HTMLImageElement} = {};

    constructor(player: Player) {
        this.player = player;
    }


    requestLoadTileset(name: string) {
        if (name in this.loadTilesetGroups)
            return;
        const group = this.loadTilesetGroups[name] = new DownloadGroup(() => {
            console.log('Tileset data loaded: ' + name);
            this.player.map.clientTilesetLoaded(name);
        });
        group.loadImageAsset(`tilesets/${name}.png`, (img) => this.tilesetImages[name] = img);
        group.finalize();
    }
}

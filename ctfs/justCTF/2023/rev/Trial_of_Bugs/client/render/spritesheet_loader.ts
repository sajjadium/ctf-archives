import {DownloadGroup} from "../download_group";
import {Player} from "../../share/game/player";
import {SpritesheetData} from "../../share/map/spritesheet_data";
import {Texture} from "./webgl/texture";

export class SpritesheetLoader { // TODO: This is different from TilesetLoader significantly for no good reason?
    private readonly gl: WebGLRenderingContext;
    private readonly player: Player;
    private readonly loadSpritesheetGroups: {[name: string]: DownloadGroup} = {};

    readonly spritesheets: {[name: string]: SpritesheetData} = {};
    readonly spritesheetTextures: {[name: string]: Texture} = {};

    constructor(gl: WebGLRenderingContext, player: Player) {
        this.gl = gl;
        this.player = player;
    }

    loadSpritesheets() {
        const targetWorld = this.player.map.targetWorld;
        if (targetWorld !== null)
            for (const name of targetWorld.loader.mapMeta.spritesheets)
                this.requestLoadSpritesheet(name);

        const currentWorld = this.player.map.currentWorld;
        for (const name of currentWorld.loader.mapMeta.spritesheets)
            this.requestLoadSpritesheet(name);

        for (const name of this.player.gameData.config.baseSpritesheets)
            this.requestLoadSpritesheet(name);
    }

    requestLoadSpritesheet(name: string) {
        if (name in this.loadSpritesheetGroups)
            return;
        const group = this.loadSpritesheetGroups[name] = new DownloadGroup(() => {
            console.log('Spritesheet data loaded: ' + name);
            this.player.map.clientSpritesheetLoaded(name);
        });
        group.loadJsonAsset(`spritesheets/${name}.json`, (data) => {
            this.spritesheets[name] = data;
            this.player.map.spritesheetData.spritesheets[name] = data;
        });
        group.loadImageAsset(`spritesheets/${name}.png`, (img) => {
            this.spritesheetTextures[name] = new Texture(this.gl, img);
        });
        group.finalize();
    }
}

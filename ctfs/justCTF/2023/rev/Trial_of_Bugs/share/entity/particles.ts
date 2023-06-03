import {Component, registerNamedComponent} from "./component";
import {SpritesheetData, SpritesheetDataManager} from "../map/spritesheet_data";

export class Particles extends Component {
    static typeName = 'particles';

    spritesheet?: string;
    particleMaxCount: number = 25;
    particleSpawnPerSecond: number = 10;
    particleLifetime: number = 1000;
    particleMinVelX: number = 0;
    particleMaxVelX: number = 0;
    particleMinVelY: number = 0;
    particleMaxVelY: number = 0;
    particleAccelX: number = 0;
    particleAccelY: number = 0;
    particleMulX: number = 1;
    particleMulY: number = 1;
    particleColorStart: {r: number, g: number, b: number, a: number} = {r: 1, g: 1, b: 1, a: 1};
    particleColorEnd: {r: number, g: number, b: number, a: number} = {r: 1, g: 1, b: 1, a: 1};
    particleSprite: string = '';


    get spritesheetData() : SpritesheetData|undefined {
        const sheets = this.world.getSingleton(SpritesheetDataManager).spritesheets;
        return sheets[this.spritesheet || ''];
    }


}
registerNamedComponent(Particles);

import {Component, registerNamedComponent} from "./component";
import {SpritesheetData, SpritesheetDataManager} from "../map/spritesheet_data";

export class Sprite extends Component {
    static typeName = 'sprite';

    spritesheet?: string;
    sprite?: string;
    layer?: number;

    get spritesheetData() : SpritesheetData|undefined {
        const sheets = this.world.getSingleton(SpritesheetDataManager).spritesheets;
        return sheets[this.spritesheet || ''];
    }


}
registerNamedComponent(Sprite);

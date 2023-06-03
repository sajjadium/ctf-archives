import {Component, registerNamedComponent} from "../entity/component";

export class MapChunkComponent extends Component {
    static typeName = 'map_chunk';

    data: number[] = [];

}
registerNamedComponent(MapChunkComponent);

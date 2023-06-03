import {Component, registerNamedComponent} from "../entity/component";
import {MapEntityLoader} from "./map_entity_loader";
import {transient} from "../util/transient";

export class MapViewZoneComponent extends Component {
    static typeName = 'map_view_zone';

    @transient private mapEntityLoader?: MapEntityLoader;

    postLoad() {
        this.register();
    }

    destroy() {
        this.unregister();
    }

    register() {
        this.mapEntityLoader = this.entity.world.getSingleton(MapEntityLoader);
        this.mapEntityLoader.viewAreas.add(this.entity.transform!);
    }

    unregister() {
        if (this.mapEntityLoader)
            this.mapEntityLoader.viewAreas.delete(this.entity.transform!);
    }

}
registerNamedComponent(MapViewZoneComponent);

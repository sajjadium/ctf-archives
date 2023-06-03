import {Component, registerNamedComponent} from "../entity/component";
import {MapEntityLoader} from "../map/map_entity_loader";
import {transient} from "../util/transient";

export class PlayerDeathComponent extends Component {
    static typeName = 'player_death';

    dying: number = -1;
    @transient enterRequested: boolean = false;
    respawnPoint: string = '';
    @transient noDeathCounter: number = 0;

    update(delta: number) {
        if (this.dying === -1)
            return;

        this.dying += delta * 5;
        if (this.dying >= 1 && this.respawnPoint !== '' && !this.enterRequested) {
            const loader = this.world.getSingleton(MapEntityLoader);
            loader.manager.requestEnterByPoint(this.world.name, loader.mapMeta.name, this.respawnPoint);
            this.enterRequested = true;
        }
    }

    onPlayerEnter() {
        this.dying = -1;
        this.enterRequested = false;
    }

    stepOnDeathTile() {
        if (this.noDeathCounter === 0)
            this.dying = 0;
    }
}
registerNamedComponent(PlayerDeathComponent);

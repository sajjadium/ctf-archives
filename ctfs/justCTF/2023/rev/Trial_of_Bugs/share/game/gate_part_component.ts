import {Component, registerNamedComponent} from "../entity/component";
import {EVENT_GLOBAL_KV_UPDATE, EVENT_PLAYER_ENTER_AREA} from "../script/event_ids";
import {EventReceiverMixin} from "../event/event_receiver";
import {EventHandlerRegistration, EventSystem} from "../event/event_system";
import {transient} from "../util/transient";
import {Player} from "./player";
import {Sprite} from "../entity/sprite";

export class GatePartComponent extends EventReceiverMixin(Component) {
    static typeName = 'gate_part';
    gameFlagName: string = '';

    @transient eventSystem?: EventSystem;
    @transient handlerRegistrations: EventHandlerRegistration[] = [];


    postLoad() {
        this.eventSystem = this.world.getSingleton(EventSystem);
        this.registerEventHandler(EVENT_GLOBAL_KV_UPDATE, {key: this.gameFlagName}, () => this.updateSprite());
        this.updateSprite();
    }

    destroy() {
        this.unregisterAllEventHandlers();
    }

    updateSprite() {
        const sprite = this.entity.getComponent(Sprite);
        const prevSpriteName = sprite.sprite!;

        const flag = this.world.getSingleton(Player).globalData.get(this.gameFlagName);
        if (flag)
            sprite.sprite = prevSpriteName.replace("_off", "_on");
        else
            sprite.sprite = prevSpriteName.replace("_on", "_off");
    }
}
registerNamedComponent(GatePartComponent);

import {Component, registerNamedComponent} from "../entity/component";
import {InputManager} from "../input/input_manager";
import {GameKey} from "../input/game_keys";
import {InteractableComponent} from "../entity/interactable_component";
import {Player} from "./player";

export class PlayerInteractionComponent extends Component {
    static typeName = 'player_interaction';

    interactPressed: boolean = false;

    update() {
        const input = this.world.getSingleton(InputManager);
        if (!input.primary.pressed[GameKey.Interact]) {
            this.interactPressed = false
            return;
        }

        if (this.interactPressed)
            return;
        this.interactPressed = true;

        const dialogue = this.world.getSingleton(Player).dialogue;
        if (dialogue.dialogueInfo.get() !== null || dialogue.choiceInfo.get() !== null)
            return;

        const bx = this.entity.transform!.centerX;
        const by = this.entity.transform!.centerY;

        const maxDist2 = Math.pow(50, 2);

        for (const entity of Object.values(this.world.entities)) {
            const interactable = entity.tryGetComponent(InteractableComponent);

            if (Math.pow(entity.transform!.centerX - bx, 2) + Math.pow(entity.transform!.centerY - by, 2) > maxDist2 &&
                !entity.transform!.intersects(this.entity.transform!))
                continue;

            if (interactable) {
                interactable.interact();
                if (dialogue.dialogueInfo.get() !== null || dialogue.choiceInfo.get() !== null)
                    return;
            }
        }
    }
}
registerNamedComponent(PlayerInteractionComponent);

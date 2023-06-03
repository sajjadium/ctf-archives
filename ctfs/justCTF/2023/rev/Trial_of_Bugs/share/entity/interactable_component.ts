import {Component, registerNamedComponent} from "../entity/component";

export class InteractableComponent extends Component {
    static typeName = 'interactable';

    interactText: string = '';

    interact() {
        for (const component of this.entity.getAllComponents() as any[]) {
            if (component.onInteract)
                component.onInteract();
        }
    }
}
registerNamedComponent(InteractableComponent);

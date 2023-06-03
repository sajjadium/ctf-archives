import {EventHandler, EventHandlerRegistration, EventSystem, EventType} from "./event_system";

type Constructor = new (...args: any[]) => {};

export function EventReceiverMixin<TBase extends Constructor>(Base: TBase) {
    return class EventReceiver extends Base {
        eventSystem?: EventSystem;
        handlerRegistrations: EventHandlerRegistration[] = [];

        registerEventHandler<T>(eventType: EventType<T>, filterData: Partial<T>, handler: EventHandler<T>): EventHandlerRegistration {
            const reg = this.eventSystem!.registerHandler(eventType, filterData, handler);
            this.handlerRegistrations.push(reg);
            return reg;
        }

        unregisterEventHandler(handler: EventHandlerRegistration) {
            this.eventSystem!.unregisterHandler(handler);
            const iof = this.handlerRegistrations.indexOf(handler);
            this.handlerRegistrations.splice(iof, 1);
        }

        unregisterAllEventHandlers() {
            for (const handler of this.handlerRegistrations)
                this.eventSystem!.unregisterHandler(handler);
            this.handlerRegistrations = [];
        }
    };
}

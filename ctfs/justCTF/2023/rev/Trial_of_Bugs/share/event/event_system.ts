export class EventType<T> {
    name: string;

    constructor(name: string) {
        this.name = name;
    }
}

export type EventInfo<T> = {
    type: EventType<T>,
    data: T
}

export type EventHandler<T> = (event: EventInfo<T>) => void;

type EventHandlerList = {
    filteredHandlers:
        {[filterKeys: string]: {
            keys: string[],
            handlers: {[key: string]: EventHandler<any>[]}
        }};
}

declare const EventHandlerRegistrationSymbol: unique symbol;
export type EventHandlerRegistration = {_opaque: typeof EventHandlerRegistrationSymbol};

type EventHandlerRegistrationNonOpaque = {
    eventType: EventType<any>,
    filterKey: string,
    filterValueString: string,
    handler: EventHandler<any>
}

function getFilterValueString(obj: any, sortedKeys: string[]) {
    return JSON.stringify(sortedKeys.map(k => obj[k]));
}

export class EventSystem {
    private handlers = new Map<EventType<any>, EventHandlerList>();

    registerHandler<T>(eventType: EventType<T>, filterData: Partial<T>, handler: EventHandler<T>): EventHandlerRegistration {
        const sortedKeys = Object.keys(filterData).sort();
        const filterKey = sortedKeys.join('|');
        const filterValueString = getFilterValueString(filterData, sortedKeys);
        const ret: EventHandlerRegistrationNonOpaque = {
            eventType,
            filterKey,
            filterValueString,
            handler
        };

        if (!this.handlers.has(eventType))
            this.handlers.set(eventType, {filteredHandlers: {}});
        const eventHandlers = this.handlers.get(eventType)!;
        if (!eventHandlers.filteredHandlers[filterKey])
            eventHandlers.filteredHandlers[filterKey] = {keys: sortedKeys, handlers: {}};
        const keyHandlers = eventHandlers.filteredHandlers[filterKey].handlers;
        if (!keyHandlers[filterValueString])
            keyHandlers[filterValueString] = [];
        keyHandlers[filterValueString].push(handler);

        return (ret as any) as EventHandlerRegistration;
    }

    unregisterHandler(handler: EventHandlerRegistration) {
        const handlerInfo = (handler as any) as EventHandlerRegistrationNonOpaque;
        const eventHandlers = this.handlers.get(handlerInfo.eventType)!;
        const keyHandlers = eventHandlers.filteredHandlers[handlerInfo.filterKey].handlers;
        const valueHandlers = keyHandlers[handlerInfo.filterValueString];
        const iof = valueHandlers.indexOf(handlerInfo.handler);
        valueHandlers.splice(iof, 1);
        if (valueHandlers.length === 0)
            delete keyHandlers[handlerInfo.filterValueString];
        if (Object.keys(keyHandlers).length === 0)
            delete eventHandlers.filteredHandlers[handlerInfo.filterKey];
        if (Object.keys(eventHandlers.filteredHandlers).length === 0)
            this.handlers.delete(handlerInfo.eventType);
    }

    emit<T>(eventType: EventType<T>, eventData: T) {
        const eventHandlers = this.handlers.get(eventType);
        if (!eventHandlers)
            return;

        const event: EventInfo<any> = {type: eventType, data: eventData};

        for (const keyHandlers of Object.values(eventHandlers.filteredHandlers)) {
            const filterValueString = getFilterValueString(eventData, keyHandlers.keys);
            const valueHandlers = keyHandlers.handlers[filterValueString];
            if (valueHandlers) {
                for (const handler of valueHandlers)
                    handler(event);
            }
        }
    }
}

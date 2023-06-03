import {EventType} from "../event/event_system";

export const EVENT_DIALOGUE_COMPLETE = new EventType<{
    interactionId: number
}>('EVENT_DIALOGUE_COMPLETE');
export const EVENT_CHOICE_COMPLETE = new EventType<{
    interactionId: number,
    choiceNum: number
}>('EVENT_CHOICE_COMPLETE');
export const EVENT_PLAYER_ENTER_AREA = new EventType<{
    worldName: string,
    areaName: string
}>('EVENT_PLAYER_ENTER_AREA');

export const EVENT_SCRIPT = new EventType<any>('EVENT_SCRIPT');

export const EVENT_GLOBAL_KV_UPDATE = new EventType<{
    key: string,
    value: any,
    oldValue: any
}>('EVENT_GLOBAL_KV_UPDATE');

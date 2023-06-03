import {ScriptManager} from "../script/script_manager";
import {NetInterface} from "../net/net_interface";
import {bothExecute, RpcSingleton} from "../net/rpc";
import {
    EVENT_CHOICE_COMPLETE,
    EVENT_DIALOGUE_COMPLETE
} from "../script/event_ids";
import {ObservableField} from "../util/observable_field";
import {EventSystem} from "../event/event_system";
import {NetIdCounter} from "../net/net_id_counter";

export type DialogueInfo = {
    interactionId: number,
    npcName: string,
    msg: string
}
export type ChoiceInfo = DialogueInfo & {
    choices: string[]
}

export class DialogueModel extends RpcSingleton {
    private eventSystem: EventSystem;
    readonly dialogueInfo = new ObservableField<DialogueInfo | null>(null);
    readonly choiceInfo = new ObservableField<ChoiceInfo | null>(null);
    private nextInteractionId;

    constructor(net: NetInterface, eventSystem: EventSystem) {
        super(net);
        this.eventSystem = eventSystem;
        this.nextInteractionId = new NetIdCounter(net);
    }

    getInteractionId() {
        return this.nextInteractionId.next();
    }

    @bothExecute({clientSync: true})
    showDialogue(interactionId: number, npcName: string, msg: string) {
        this.dialogueInfo.set({interactionId, npcName, msg});
        return interactionId;
    }

    @bothExecute({clientInvokable: true, clientSync: true})
    completeDialogue() {
        const info = this.dialogueInfo.get();
        if (!info)
            return;
        this.dialogueInfo.set(null);
        this.eventSystem.emit(EVENT_DIALOGUE_COMPLETE, {interactionId: info.interactionId});
    }

    @bothExecute({clientSync: true})
    showChoice(interactionId: number, npcName: string, msg: string, choices: string[]) {
        this.choiceInfo.set({interactionId, npcName, msg, choices});
        return interactionId;
    }

    @bothExecute({clientInvokable: true, clientSync: true})
    completeChoice(choiceNum: number) {
        const info = this.choiceInfo.get();
        if (!info)
            return;
        this.choiceInfo.set(null);
        this.eventSystem.emit(EVENT_CHOICE_COMPLETE, {interactionId: info.interactionId, choiceNum});
    }
}


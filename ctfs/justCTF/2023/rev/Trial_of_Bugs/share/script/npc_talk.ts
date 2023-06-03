import {
    Opcode,
    ParamBlockNum,
    ParamId,
    ParamStr,
    registerOpcode
} from "./opcode_base";
import {EvalCtx, PlayerEvalCtx} from "./eval_ctx";
import {EVENT_CHOICE_COMPLETE, EVENT_DIALOGUE_COMPLETE} from "./event_ids"
import {applyFormat} from "./text_format";
import {registerTask, ScriptTask} from "./task";


const INTERNAL_NPC_NAME = "npcname";


class OpSetName implements Opcode {
    name = "SETNAME"
    params = [ParamId, ParamStr]

    exec(ctx: EvalCtx, id: string, str: string) {
        ctx.setInternal(INTERNAL_NPC_NAME, id, str);
    }
}
export const OP_SETNAME = registerOpcode(OpSetName);


class OpDialogue implements Opcode {
    name = "DIALOGUE"
    params = [ParamId, ParamStr]

    exec(ctx: EvalCtx, id: string, str: string) {
        const npcName = ctx.getInternal(INTERNAL_NPC_NAME, id);
        ctx.beginTaskFromProps(NpcTalkTask, {npcName, text: applyFormat(str, ctx.jsProps)});
    }
}
export const OP_DIALOGUE = registerOpcode(OpDialogue);

class NpcTalkTask extends ScriptTask {
    static typeName = 'npc_talk';

    npcName!: string;
    text!: string;

    description?: string = 'Finish the dialogue';

    onResume() {
        const dialogue = (this.ctx as PlayerEvalCtx).player.dialogue;
        const interactionId = dialogue.getInteractionId();
        dialogue.showDialogue(interactionId, this.npcName, this.text);
        this.registerEventHandler(EVENT_DIALOGUE_COMPLETE, {interactionId}, () => this.end());
    }
}

registerTask(NpcTalkTask);


class OpChoice implements Opcode {
    name = "CHOICE"
    params = [ParamId, ParamStr, ParamStr, ParamBlockNum] // TODO

    exec(ctx: EvalCtx, id: string, str: string, labels: string[], blocks: number[]) {
        const npcName = ctx.getInternal(INTERNAL_NPC_NAME, id);
        labels = labels.map(x => applyFormat(x, ctx.jsProps));
        ctx.beginTaskFromProps(NpcChoiceTask, {npcName, text: applyFormat(str, ctx.jsProps), labels});
    }
}
export const OP_CHOICE = registerOpcode(OpChoice);

class NpcChoiceTask extends ScriptTask {
    static typeName = 'npc_choice';

    npcName!: string;
    text!: string;
    labels!: string[];

    description?: string = 'Finish the dialogue';

    onResume() {
        const blocks = this.ctx.getCurrentOpcodeArg(3);

        const dialogue = (this.ctx as PlayerEvalCtx).player.dialogue;
        const interactionId = dialogue.getInteractionId();
        dialogue.showChoice(interactionId, this.npcName, this.text, this.labels);
        this.registerEventHandler(EVENT_CHOICE_COMPLETE, {interactionId}, e => {
            const blockNo = blocks[e.data.choiceNum];
            if (blockNo === undefined)
                throw new Error("Invalid choice");
            const block = this.ctx.blob.blocks[blockNo];

            this.ctx.nextEvalInfo = {block, blockNo, insnNo: 0, parent: this.ctx.nextEvalInfo};
            this.end();
        });
    }
}

registerTask(NpcChoiceTask);

import {Opcode} from "./opcode_base";
import {EvalCtx} from "./eval_ctx";

export class ScriptEvaluator {
    static start(ctx: EvalCtx, blockLabel: string) {
        this.startById(ctx, ctx.blob.blockLabels[blockLabel]);
    }

    static startById(ctx: EvalCtx, blockNo: number) {
        const block = ctx.blob.blocks[blockNo];
        ctx.evalInfo = {block, blockNo, insnNo: 0};
    }

    static update(ctx: EvalCtx) {
        if (ctx.evalPaused)
            return true;
        if (ctx.nextEvalInfo) {
            ctx.evalInfo = ctx.nextEvalInfo;
            ctx.nextEvalInfo = undefined;
        }
        while (ctx.evalInfo) {
            const {block, insnNo} = ctx.evalInfo;
            if (insnNo >= block.length) {
                ctx.evalInfo = ctx.evalInfo.parent;
                continue;
            }
            const opcode: Opcode = block[insnNo];
            switch (opcode.params.length) {
                case 0:
                    opcode.exec(ctx);
                    break;
                case 1:
                    opcode.exec(ctx, block[insnNo + 1]);
                    break;
                case 2:
                    opcode.exec(ctx, block[insnNo + 1], block[insnNo + 2]);
                    break;
                case 3:
                    opcode.exec(ctx, block[insnNo + 1], block[insnNo + 2], block[insnNo + 3]);
                    break;
                case 4:
                    opcode.exec(ctx, block[insnNo + 1], block[insnNo + 2], block[insnNo + 3], block[insnNo + 4]);
                    break;
                default:
                    throw new Error('bad opcode arg count');
            }
            if (ctx.evalPaused) {
                ctx.nextEvalInfo = {...ctx.evalInfo};
                ctx.nextEvalInfo.insnNo += 1 + opcode.params.length;
                break;
            } else if (ctx.nextEvalInfo) {
                ctx.evalInfo = ctx.nextEvalInfo;
                ctx.nextEvalInfo = undefined;
            } else {
                ctx.evalInfo.insnNo += 1 + opcode.params.length;
            }
        }
        return !!ctx.evalInfo;
    }

    static dispatchEvent(eventId: number, eventData: string) {
        //
    }
}

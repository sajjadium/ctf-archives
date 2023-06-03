import {
    Opcode,
    ParamBlockNum,
    ParamJsCodeNum,
    registerOpcode
} from "./opcode_base";
import {EvalCtx} from "./eval_ctx";

class OpCall implements Opcode {
    name = "CALL"
    params = [ParamBlockNum]

    exec(ctx: EvalCtx, id: number) {
        const block = ctx.blob.blocks[id];
        ctx.evalInfo!.insnNo += 1 + this.params.length;
        ctx.nextEvalInfo = {block, blockNo: id, insnNo: 0, parent: ctx.evalInfo};
    }
}
export const OP_CALL = registerOpcode(OpCall);


class OpJsExec implements Opcode {
    name = "JSEXEC"
    params = [ParamJsCodeNum]

    exec(ctx: EvalCtx, id: number) {
        ctx.blob.jsCode![id](ctx.jsProps);
    }
}
export const OP_JSEXEC = registerOpcode(OpJsExec);


class OpJsIf implements Opcode {
    name = "JSIF"
    params = [ParamJsCodeNum, ParamBlockNum, ParamBlockNum] // TODO

    exec(ctx: EvalCtx, codeIds: number[], codeBlocks: number[], elseBlock: number) {
        let targetBlockNo = elseBlock;
        for (let i = 0; i < codeIds.length; i++) {
            const ret = ctx.blob.jsCode![codeIds[i]](ctx.jsProps);
            if (ret) {
                targetBlockNo = codeBlocks[i];
                break;
            }
        }

        if (targetBlockNo === -1)
            return;

        const block = ctx.blob.blocks[targetBlockNo];
        ctx.evalInfo!.insnNo += 1 + this.params.length;
        ctx.nextEvalInfo = {block, blockNo: targetBlockNo, insnNo: 0, parent: ctx.evalInfo};
    }
}
export const OP_JSIF = registerOpcode(OpJsIf);

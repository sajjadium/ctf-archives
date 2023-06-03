import {EvalCtx} from "./eval_ctx";
import {NetInterface} from "../net/net_interface";
import {ScriptEvaluator} from "./evaluator";
import {ScriptHolder} from "./script_holder";

export type ScriptManagerSaveData = {
    nextScriptEvalId: number
}

export class ScriptManager {
    private net: NetInterface;
    private scripts: {[id: number]: {ctx: EvalCtx, holder: ScriptHolder}} = {};
    private nextScriptEvalId: number = 0;
    private executingScript: boolean = false;
    private executeQueue: EvalCtx[] = [];

    constructor(net: NetInterface) {
        this.net = net;
    }

    save(): ScriptManagerSaveData {
        return {
            nextScriptEvalId: this.nextScriptEvalId
        };
    }

    load(data: ScriptManagerSaveData) {
        this.nextScriptEvalId = data.nextScriptEvalId;
    }

    addScript(ctx: EvalCtx, holder: ScriptHolder, blockLabel: string) {
        if (ctx.evalId !== undefined)
            throw new Error("Context already has a script evaluation ID");
        ctx.evaluator = this;
        ctx.evalId = this.nextScriptEvalId++;
        this.scripts[ctx.evalId] = {ctx, holder};
        holder.onAddScript(ctx);

        ScriptEvaluator.start(ctx, blockLabel);
        this.continueScript(ctx);
    }

    addLoadedScript(ctx: EvalCtx, holder: ScriptHolder) {
        if (ctx.evalId === undefined)
            throw new Error("Context must already have an eval id set");
        ctx.evaluator = this;
        this.scripts[ctx.evalId] = {ctx, holder};
        holder.onAddScript(ctx);

        this.continueScript(ctx);
    }

    continueScript(ctx: EvalCtx) {
        if (this.executingScript) {
            this.executeQueue.push(ctx);
            return;
        }

        this.executingScript = true;
        if (!ScriptEvaluator.update(ctx))
            this.removeScript(ctx);
        if (this.executeQueue.length > 0) {
            for (let i = 0; i < this.executeQueue.length; i++) {
                if (!ScriptEvaluator.update(this.executeQueue[i]))
                    this.removeScript(this.executeQueue[i]);
            }
            this.executeQueue = [];
        }
        this.executingScript = false;
    }

    removeScript(ctx: EvalCtx) {
        ctx.endTask();
        this.scripts[ctx.evalId!].holder.onRemoveScript(ctx);
        delete this.scripts[ctx.evalId!];
    }
}

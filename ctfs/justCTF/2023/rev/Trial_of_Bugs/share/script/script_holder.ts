import {ScriptManager} from "./script_manager";
import {EvalCtx} from "./eval_ctx";

export class ScriptHolder {
    private readonly manager: ScriptManager;
    readonly scripts: {[id: number]: EvalCtx} = {};
    private readonly ctxFactory: () => EvalCtx;

    constructor(manager: ScriptManager, ctxFactory: () => EvalCtx) {
        this.manager = manager;
        this.ctxFactory = ctxFactory;
    }

    load(data: any) {
        for (const entry of data) {
            const ctx = this.ctxFactory();
            ctx.load(entry);
            this.manager.addLoadedScript(ctx, this);
        }
    }

    save(): any {
        return Object.values(this.scripts).map(x => x.save());
    }

    addScript(blockLabel: string) {
        const ctx = this.ctxFactory();
        this.manager.addScript(ctx, this, blockLabel);
        return ctx;
    }

    onAddScript(ctx: EvalCtx) {
        this.scripts[ctx.evalId!] = ctx;
    }

    onRemoveScript(ctx: EvalCtx) {
        delete this.scripts[ctx.evalId!];
    }
}

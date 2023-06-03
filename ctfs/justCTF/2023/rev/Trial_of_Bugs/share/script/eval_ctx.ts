import {ScriptBlob} from "./blob";
import {Opcode} from "./opcode_base";
import {Player} from "../game/player";
import {knownScriptTasks, ScriptTask} from "./task";
import {EventSystem} from "../event/event_system";
import {tasks} from "./tasks";
import {EVENT_SCRIPT} from "./event_ids";

const INTERNAL_JS = "js";


type NonFunctionPropertyNames<T> = {
    [K in keyof T]: T[K] extends Function ? never : K
}[keyof T];

type EvalInsnInfo = {
    block: any[];
    blockNo: number,
    insnNo: number;
    parent?: EvalInsnInfo|undefined;
};

export interface ScriptEvaluator {
    continueScript(ctx: EvalCtx): void;
}


function saveEvalInfo(evalInfo: EvalInsnInfo|undefined): any {
    return evalInfo ? [evalInfo.blockNo, evalInfo.insnNo, saveEvalInfo(evalInfo.parent)] : null;
}
function loadEvalInfo(blob: ScriptBlob, data: any): EvalInsnInfo|undefined {
    if (data !== null)
        return {block: blob.blocks[data[0]], blockNo: data[0], insnNo: data[1], parent: loadEvalInfo(blob, data[2])};
    return undefined;
}

export class EvalCtx {
    private readonly internals: {[internalType: string]: {[key: string]: any}}
    private internalDiff: {[internalType: string]: {[key: string]: any}} | null;

    evaluator: ScriptEvaluator|undefined;
    evalId: number|undefined;
    blob: ScriptBlob;
    eventSystem?: EventSystem;
    evalInfo: EvalInsnInfo|undefined;
    nextEvalInfo: EvalInsnInfo|undefined;
    evalPaused: boolean;
    readonly jsProps: any;
    task: ScriptTask|undefined;

    constructor(blob: ScriptBlob) {
        this.evaluator = undefined;
        this.evalId = undefined;
        this.blob = blob;
        this.internals = {};
        this.internalDiff = null;
        this.evalInfo = undefined;
        this.nextEvalInfo = undefined;
        this.evalPaused = false;
        this.task = undefined;

        const self = this;
        this.jsProps = new Proxy({}, {
            get(target: {}, p: string | symbol, receiver: any): any {
                const contextVar = self.getContextVar(p.toString());
                if (contextVar)
                    return contextVar;
                return self.getInternal(INTERNAL_JS, p.toString());
            },
            set(target: {}, p: string | symbol, newValue: any, receiver: any): boolean {
                self.setInternal(INTERNAL_JS, p.toString(), newValue);
                return true;
            },
            ownKeys(target: {}): ArrayLike<string | symbol> {
                if (self.internals[INTERNAL_JS] !== undefined)
                    return Object.keys(self.internals[INTERNAL_JS]);
                return [];
            }
        })
    }

    save() {
        return {
            evalId: this.evalId,
            internals: this.internals,
            evalInfo: saveEvalInfo(this.evalInfo),
            nextEvalInfo: saveEvalInfo(this.nextEvalInfo),
            evalPaused: this.evalPaused ? true : undefined,
            taskName: (this.task?.constructor as any)?.typeName,
            task: this.task?.save()
        }
    }

    load(data: any) {
        this.evalId = data.evalId;
        Object.assign(this.internals, data.internals);
        this.evalInfo = loadEvalInfo(this.blob, data.evalInfo);
        this.nextEvalInfo = loadEvalInfo(this.blob, data.nextEvalInfo);
        if (data.evalPaused)
            this.evalPaused = true;
        if (data.taskName)
            this.beginTaskFromProps(data.taskName, data.task, true);
    }

    startSinglePartyExecution() {
        this.internalDiff = {};
    }

    finishSinglePartyExecution() {
        const ret = {
            'internal': this.internalDiff
        };
        this.internalDiff = null;
        return ret;
    }

    getCurrentOpcode(): Opcode|null {
        if (this.evalInfo === undefined)
            return null;
        return this.evalInfo.block[this.evalInfo.insnNo];
    }

    getCurrentOpcodeArg(no: number): any {
        if (this.evalInfo === undefined)
            return null;
        return this.evalInfo.block[this.evalInfo.insnNo + 1 + no];
    }

    beginTask(task: ScriptTask, skipBegin: boolean = false) {
        this.task = task;
        this.evalPaused = true;
        task.ctx = this;
        task.eventSystem = this.eventSystem;
        task.earlyInit();
        if (!skipBegin)
            task.onBegin();
        task.onResume();
    }

    beginTaskFromProps<T extends ScriptTask>(task: (new () => T), props: Omit<Pick<T, NonFunctionPropertyNames<T>>, 'ctx' | 'eventSystem' | 'handlerRegistrations'>): void;
    beginTaskFromProps(name: string, props: any): void;
    beginTaskFromProps(name: string, props: any, skipBegin: boolean): void;

    beginTaskFromProps(name: (new () => ScriptTask) | string, props: any, skipBegin: boolean = false) {
        const taskInstance = typeof name === 'string' ? new knownScriptTasks[name]() : new name();
        taskInstance.load(props);
        this.beginTask(taskInstance, skipBegin);
    }

    endTask() {
        if (!this.task)
            return;
        this.task.onEnd();
        this.task = undefined;
        this.resumeEval();
    }

    pauseEval() {
        this.evalPaused = true;
    }

    resumeEval() {
        this.evalPaused = false;
    }

    setInternal(internalType: string, name: string, value: any) {
        if (this.internals[internalType] === undefined)
            this.internals[internalType] = {};
        this.internals[internalType][name] = value;

        if (this.internalDiff !== null) {
            if (this.internalDiff[internalType] === undefined)
                this.internalDiff[internalType] = {};
            this.internalDiff[internalType][name] = value;
        }
    }

    getInternal(internalType: string, name: string): any {
        if (this.internals[internalType] === undefined)
            return undefined;
        return this.internals[internalType][name];
    }

    protected getContextVar(name: string): any {
        if (name === 'emit')
            return (t: any) => this.eventSystem?.emit(EVENT_SCRIPT, t);
        if (name === 'task')
            return (t: any) => this.beginTask(t);
        if (name === 'tasks')
            return tasks;
        return undefined;
    }
}

export class PlayerEvalCtx extends EvalCtx {
    player: Player;

    constructor(blob: ScriptBlob, player: Player) {
        super(blob);
        this.player = player;
        this.eventSystem = player.eventSystem;
    }

    protected getContextVar(name: string): any {
        if (name === 'player')
            return this.player;
        return super.getContextVar(name);
    }
}

// Usable only for non-persistent scripts.
export class StaticEvalCtx extends EvalCtx {
    jsContext: any = {};

    protected getContextVar(name: string): any {
        return this.jsContext[name];
    }
}

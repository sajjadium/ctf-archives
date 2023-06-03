import {EvalCtx} from "./eval_ctx";
import {stripTransientProperties, transient} from "../util/transient";
import {EventReceiverMixin} from "../event/event_receiver";
import {EventHandlerRegistration, EventSystem} from "../event/event_system";

export class ScriptTask extends EventReceiverMixin(Object) {
    @transient eventSystem?: EventSystem;
    @transient handlerRegistrations: EventHandlerRegistration[] = [];
    @transient ctx!: EvalCtx;
    @transient endCallback?: () => void;

    description?: string;

    load(data: any) {
        Object.assign(this, data);
    }

    save() {
        return stripTransientProperties(this);
    }

    earlyInit() {
    }

    onBegin() {
    }

    onResume() {
    }

    onPause() {
    }

    onEnd() {
        this.unregisterAllEventHandlers();
    }

    end() {
        if (this.endCallback) {
            this.endCallback();
        } else {
            this.ctx.endTask();
            this.ctx.evaluator?.continueScript(this.ctx);
        }
    }
}

export type NamedScriptTask = (new () => ScriptTask) & {
    typeName: string;
}

export const knownScriptTasks: {[name: string]: NamedScriptTask} = {};

export function registerTask(task: NamedScriptTask) {
    knownScriptTasks[task.typeName] = task;
}

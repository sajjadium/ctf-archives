import {knownScriptTasks, ScriptTask} from "./task";
import {stripTransientProperties, transient} from "../util/transient";

export type CompletedTaskInfo = {
    description?: string;
}

export abstract class WrapperTask extends ScriptTask {
    @transient private subtaskList: (ScriptTask|null)[] = [];
    completedSubtasks: (CompletedTaskInfo|null)[] = [];

    get subtasks() {
        return this.subtaskList;
    }

    setSubtasks(subtasks: (ScriptTask|null)[]) {
        this.subtaskList = subtasks;
        for (let i = 0; i < this.subtaskList.length; i++) {
            const subtask = this.subtaskList[i];
            if (subtask) {
                subtask.eventSystem = this.eventSystem;
                subtask.ctx = this.ctx;
                subtask.endCallback = this.onSubtaskEnded.bind(this, i);
            }
        }
    }

    earlyInit() {
        this.setSubtasks(this.subtaskList);
    }

    onSubtaskEnded(index: number) {
        this.completedSubtasks[index] = {description: this.subtaskList[index]!.description};
        this.subtaskList[index]!.onEnd();
        this.subtaskList[index] = null;
    }

    load(data: any) {
        super.load(data);
        if (data._subtasks) {
            delete (this as any)._subtasks;
            this.setSubtasks(data._subtasks.map((x: any) => {
                if (!x)
                    return null;
                const subtask = new knownScriptTasks[x[0]]();
                subtask.load(x[1]);
                return subtask;
            }));
        }
    }

    save(): any {
        const ret = stripTransientProperties(this, true);
        ret._subtasks = this.subtasks.map(x => x ? [(x.constructor as any).typeName, x.save()] : null);
        return ret;
    }

    onBegin() {
        for (const task of this.subtasks) {
            task?.onBegin();
        }
    }

    onResume() {
        for (const task of this.subtasks)
            task?.onResume();
    }

    onPause() {
        for (const task of this.subtasks)
            task?.onPause();
    }

    onEnd() {
        for (const task of this.subtasks)
            task?.onEnd();
    }
}

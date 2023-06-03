import {EvalCtx} from "./eval_ctx";

export interface Opcode {
    name: string;
    params: OpParam[];

    exec(ctx: EvalCtx, ...args: any): void;
}

export const opcodes: {[name: string]: Opcode} = {};
export function registerOpcode<T extends Opcode>(t: new () => T): T {
    const ret = new t();
    opcodes[ret.name] = ret;
    return ret;
}


export interface OpParam {
}

export class ParamBlockNum implements OpParam {
    val: number;

    constructor(val: number) {
        this.val = val;
    }
}
export class ParamJsCodeNum implements OpParam {
    val: number;

    constructor(val: number) {
        this.val = val;
    }
}
export class ParamId implements OpParam {
    val: string;

    constructor(val: string) {
        this.val = val;
    }
}
export class ParamStr implements OpParam {
    val: string;

    constructor(val: string) {
        this.val = val;
    }
}


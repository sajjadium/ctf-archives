import {Opcode, opcodes} from "./opcode_base";
import "./opcodes";

export type JsonScriptBlob = {
    opcodes: string[],
    blocks: any[],
    blockLabels: {[name: string]: number}
};

export type ScriptBlobJsGlobal = ((ctx: any) => any)[];

export class ScriptBlob {
    blocks: any[][];
    blockLabels: {[name: string]: number};
    jsCode?: ScriptBlobJsGlobal;

    constructor(blocks: any[][], blockLabels: {[name: string]: number}) {
        this.blocks = blocks;
        this.blockLabels = blockLabels;
    }

    static fromJson(data: JsonScriptBlob): ScriptBlob {
        const lOpcodes: Opcode[] = data.opcodes.map(x => opcodes[x]);

        const blocks = [];
        for (const origBlock of data.blocks) {
            const block = [...origBlock];
            for (let i = 0; i < block.length; ) {
                let opcode: Opcode = lOpcodes[block[i]];
                block[i] = opcode;
                i += 1 + opcode.params.length;
            }
            blocks.push(block);
        }
        return new ScriptBlob(blocks, data.blockLabels);
    }

    toJson() {
        let opcodeCounts: {[key: string]: number} = {};
        for (const block of this.blocks) {
            for (let i = 0; i < block.length; ) {
                let opcode: Opcode = block[i];
                if (opcodeCounts[opcode.name] === undefined)
                    opcodeCounts[opcode.name] = 0;
                ++opcodeCounts[opcode.name];
                i += 1 + opcode.params.length;
            }
        }
        const opcodes = Object.entries(opcodeCounts)
            .sort((a, b) => b[1] - a[1])
            .map(x => x[0]);
        const opcodeMap = Object.fromEntries(opcodes.map((x, i) => [x, i]));
        const ret: JsonScriptBlob = {
            opcodes: opcodes,
            blocks: [],
            blockLabels: this.blockLabels
        };
        for (const origBlock of this.blocks) {
            const block = [...origBlock];
            for (let i = 0; i < block.length; ) {
                let opcode: Opcode = block[i];
                block[i] = opcodeMap[opcode.name];
                i += 1 + opcode.params.length;
            }
            ret.blocks.push(block);
        }
        return ret;
    }
}

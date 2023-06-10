export interface Change {
    index: number;
    remove: number;
    insert: Uint8Array;
}

export interface Block {
    prevHash: bigint;
    changes: Change[];
}

export const blockToBuf = (block: Block): Buffer => {
    let currOutputStr = block.prevHash.toString(16).padStart(32, "0");
    currOutputStr += "|";
    currOutputStr += block.changes.length.toString(16);
    currOutputStr += ":";

    for (const change of block.changes) {
        currOutputStr += "[@";
        currOutputStr += change.index.toString(16);
        currOutputStr += "-";
        currOutputStr += change.remove.toString(16);
        currOutputStr += "+";
        currOutputStr += change.insert.byteLength.toString(16);
        currOutputStr += "(";
        for (const byte of change.insert) currOutputStr += byte.toString(16).padStart(2, '0');
        currOutputStr += ")]";
    }

    return Buffer.from(currOutputStr);
}

const parseBigint = (str: string, radix: number): bigint | null => {
    const order = "0123456789abcdefghijklmnopqrstuvwxyz";

    let curr = 0n;

    for (const char of str) {
        const number = order.indexOf(char.toLowerCase());

        if (number === -1) return null;

        curr *= BigInt(radix);
        curr += BigInt(number);
    }

    return curr;
}

export const bufToBlock = (buffer: Buffer): Block | null => {
    let remaining = buffer;


    const prevHash = parseBigint(buffer.subarray(0, 32).toString("ascii"), 16);
    if (prevHash === null) return null;

    remaining = remaining.subarray(33);
    
    const end = remaining.indexOf(':', 0, 'ascii');
    if (end === -1) return null;
    
    const numChanges = parseInt(remaining.subarray(0, end).toString("ascii"), 16);
    if (!numChanges) return null;
    
    remaining = remaining.subarray(end + 1);
    const changes: Change[] = [];


    for (let i = 0; i < numChanges; i++) {
        const remove = remaining.indexOf('-', 0, 'ascii');
        const add = remaining.indexOf('+', 0, 'ascii');
        const data = remaining.indexOf('(', 0, 'ascii');
        const dataend = remaining.indexOf(')]', 0, 'ascii');

        if (remove === -1 || add === -1 || data === -1 || dataend === -1) return null;

        const index = parseInt(remaining.subarray(2, remove).toString('ascii'), 16);
        const removeCount = parseInt(remaining.subarray(remove + 1, add).toString('ascii'), 16);
        const addCount = parseInt(remaining.subarray(add + 1, data).toString('ascii'), 16);
        const dataContents = remaining.subarray(data + 1, dataend);

        if (
            Number.isNaN(index) || Number.isNaN(removeCount) ||
            Number.isNaN(addCount) || addCount !== dataContents.byteLength / 2
        ) return null;

        const dataArr = [];

        for (let j = 0; j < addCount; j++) {
            const byte = parseInt(dataContents.subarray(j * 2, j * 2 + 2).toString('ascii'), 16);
            if (Number.isNaN(byte) || byte > 255 || byte < 0) return null;

            dataArr.push(byte);
        }

        changes.push({ index, remove: removeCount, insert: new Uint8Array(dataArr) });

        remaining = remaining.subarray(dataend + 2);
    }

    if (remaining.length !== 0) return null;

    return {
        prevHash,
        changes,
    };
};

export const execBlock = (data: number[], block: Block) => {
    let currData = [...data];
    for (const change of block.changes) {
        const newData = [...currData];
        if (newData.length < change.index) return currData;
        
        newData.splice(change.index, change.remove, ...change.insert);
        currData = newData;
    }
    return currData;
};

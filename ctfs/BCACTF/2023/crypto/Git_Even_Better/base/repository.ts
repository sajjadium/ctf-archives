import { Block, Change, blockToBuf, bufToBlock, execBlock } from "./block";
import myHashFunction from "./hashing";

interface Repository {
    blocks: Map<bigint, string>;
    mostRecent: bigint;
}

export const newRepo = (): Repository => ({ blocks: new Map(), mostRecent: 0n });

export const withBlock = (repo: Repository, block: Block): Repository => ({
    mostRecent: repo.mostRecent,
    blocks: new Map([
        ...repo.blocks.entries(),
        [myHashFunction(blockToBuf(block)), blockToBuf(block).toString('ascii')]
    ]),
});

export const blocks = (repo: Repository): [bigint, string][] | null => {
    const blocks: [bigint, string][] = [];

    let currBlock = repo.mostRecent;

    while (currBlock !== 0n) {
        const data = repo.blocks.get(currBlock);
        if (!data) return null;

        blocks.unshift([currBlock, data]);

        const block = bufToBlock(Buffer.from(data));
        if (!block) return null;
        currBlock = block.prevHash; 
    }

    return blocks;
};
export const fromBlocks = (blocks: Block[]): Repository => ({
    blocks: new Map(blocks.map(
        block => [myHashFunction(blockToBuf(block)), blockToBuf(block).toString('ascii')]
    )),
    mostRecent: myHashFunction(blockToBuf(blocks[blocks.length - 1])),
});

export const appended = (repo: Repository, changes: Change[]): Repository => {
    const block: Block = { prevHash: repo.mostRecent, changes };

    return {
        ...withBlock(repo, block),
        mostRecent: myHashFunction(blockToBuf(block)),
    };
};

export const build = (repo: Repository): Buffer | null => {
    const listOfBlocksToExecute = [];
    let currBlock = repo.mostRecent;

    while (currBlock !== 0n) {
        const data = repo.blocks.get(currBlock);
        if (!data) return null;

        const block = bufToBlock(Buffer.from(data));
        if (!block) return null;

        listOfBlocksToExecute.unshift(block);
        currBlock = block.prevHash;
    }

    const array = listOfBlocksToExecute.reduce((curr, block) => execBlock(curr, block), [] as number[]);

    return Buffer.from(array);
};

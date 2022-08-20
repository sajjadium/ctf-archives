// SPDX-License-Identifier: UNLICENSED

// Challenge author: stong (cts), Zellic Inc.
// Challenge prepared for Paradigm CTF 2022

pragma solidity ^0.8.13;

import "./Opcodes.sol";

struct BasicBlock {
    uint start;
    uint end;
    uint dst1;
    uint dst2;
}

uint constant INVALID_ADDR = 0xffffffffffffffffffffffffffffffffffffff;

// Relocation info
struct CodeLabel {
    uint bytecodeOffset;
    uint dstBlock;
}

// For more documentation, please see https://en.wikipedia.org/wiki/Just-in-time_compilation
//
// We apologize for any bugs in our compiler software.
contract JIT {
    mapping (uint => uint) private loops;
    uint[] private stack; // loop stack

    // Control flow graph
    BasicBlock[] private blocks;

    // Codegen
    CodeLabel[] private labels;
    mapping (uint => uint) private basicBlockAddrs;

    uint8[] code;

    function invoke(bytes calldata _program, bytes calldata stdin) public {
        bytes memory program = bytes(_program);

        code = [
            OP_PUSH4, 0, 0, 0, 0, // length
            OP_DUP1,
            OP_PUSH1, 14, // offset
            OP_PUSH1, 0, // destoffset
            OP_CODECOPY,
            OP_PUSH1, 0,
            OP_RETURN
        ];

        uint constructorCodeSize = code.length;

        // Control flow analysis
        {
            // Pass 1: Jump target analysis
            for (uint i = 0; i < program.length; i++) {
                bytes1 op = program[i];
                if (op == "[") {
                    stack.push(i);
                } else if (op == "]") {
                    uint j = stack[stack.length-1];
                    stack.pop();
                    loops[i] = j;
                    loops[j] = i;
                }
            }
            delete stack;

            // Pass 2: Build control flow graph
            BasicBlock memory curBlock = BasicBlock({start: 0, end: INVALID_ADDR, dst1: INVALID_ADDR, dst2: INVALID_ADDR});
            for (uint i = 0; i < program.length; i++) {
                bytes1 op = program[i];
                if (op == "[") {
                    if (curBlock.start != i) {
                        // curBlock is non-empty
                        curBlock.end = i;
                        curBlock.dst1 = i; // loop entry edge
                        blocks.push(curBlock);
                    } // otherwise, if empty, just discard the empty curBlock
                    blocks.push(BasicBlock({start: i, end: i+1, dst1: i+1, dst2: loops[i]+1})); // loop header block
                    curBlock = BasicBlock({start: i+1, end: INVALID_ADDR, dst1: INVALID_ADDR, dst2: INVALID_ADDR});
                } else if (op == "]") {
                    curBlock.end = i+1;
                    curBlock.dst1 = loops[i]; // back edge
                    blocks.push(curBlock);
                    curBlock = BasicBlock({start: i+1, end: INVALID_ADDR, dst1: INVALID_ADDR, dst2: INVALID_ADDR});
                }
            }
            if (curBlock.start != program.length) {
                curBlock.end = program.length;
                blocks.push(curBlock);
            }
        }

        // Peephole optimization pass
        {
            // Contraction (++++ -> A4##, >>>> -> R4##)
            for (uint i = 0; i < blocks.length; i++) {
                BasicBlock memory bb = blocks[i];
                bytes1 prevOp = "#";
                uint repeat = 0;
                for (uint j = bb.start; j < bb.end; j++) {
                    bytes1 op = program[j];
                    if (op == "#") continue;
                    if (op == prevOp) {
                        repeat++;
                    } else {
                        if (repeat > 2) {
                            bytes1 newOp = 0;
                            if (prevOp == ">") {
                                newOp = "R";
                            } else if (prevOp == "<") {
                                newOp = "L";
                            } else if (prevOp == "+") {
                                newOp = "A";
                            } else if (prevOp == "-") {
                                newOp = "S";
                            }
                            if (newOp != 0) {
                                program[j - repeat] = newOp;
                                program[j - repeat + 1] = bytes1(uint8(repeat >> 8));
                                program[j - repeat + 2] = bytes1(uint8(repeat));
                                for (uint k = 0; k < repeat - 3; k++) {
                                    program[j - repeat + 3 + k] = '#'; // no-op
                                }
                            }
                        }
                        prevOp = op;
                        repeat = 1;
                    }
                }
            }

            // Clear loops [-] -> 0##
            for (uint i = 0; i < blocks.length; i++) {
                BasicBlock memory bb = blocks[i];
                if (bb.end == bb.start + 2 && bb.dst1 + 1 == bb.start) {
                    if (program[bb.start] == "-" && program[bb.start+1] == "]") {
                        if (program[bb.dst1] != "[") revert("invalid code");
                        program[bb.dst1] = "0";
                        program[bb.start] = "#";
                        program[bb.start+1] = "#";
                    }
                }
            }
        }

        // Code generation
        //
        // Stack layout
        //
        // <scratch space>
        // <ptr>
        // <io_ptr>
        //
        // Memory layout
        //
        // VM memory begins at 0x8000
        {
            // Pass 1. Lowering

            code.push(OP_PUSH1); code.push(0); // io_ptr := 0
            code.push(OP_PUSH2); code.push(0x80); code.push(0x00); // ptr := 0x8000

            for (uint i = 0; i < blocks.length; i++) {
                BasicBlock memory bb = blocks[i];

                basicBlockAddrs[bb.start] = code.length - constructorCodeSize;
                code.push(OP_JUMPDEST);

                for (uint j = bb.start; j < bb.end; j++) {
                    bytes1 op = program[j];

                    // Standard ops
                    if (op == ">") {
                        code.push(OP_PUSH1); code.push(32);
                        code.push(OP_ADD);
                    } else if (op == "<") {
                        code.push(OP_PUSH1); code.push(32);
                        code.push(OP_SWAP1);
                        code.push(OP_SUB);
                    } else if (op == "+") {
                        code.push(OP_DUP1);
                        code.push(OP_MLOAD);
                        code.push(OP_PUSH1); code.push(1);
                        code.push(OP_ADD);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);
                    } else if (op == "-") {
                        code.push(OP_DUP1);
                        code.push(OP_MLOAD);
                        code.push(OP_PUSH1); code.push(1);
                        code.push(OP_SWAP1);
                        code.push(OP_SUB);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);
                    } else if (op == ".") {
                        code.push(OP_PUSH1); code.push(1);
                        code.push(OP_DUP2);
                        code.push(OP_PUSH1); code.push(31);
                        code.push(OP_ADD);
                        code.push(OP_LOG0);
                    } else if (op == ",") {
                        code.push(OP_DUP2);
                        code.push(OP_CALLDATALOAD);
                        code.push(OP_PUSH1); code.push(248);
                        code.push(OP_SHR);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);

                        code.push(OP_SWAP1);
                        code.push(OP_PUSH1); code.push(1);
                        code.push(OP_ADD);
                        code.push(OP_SWAP1);
                    } else if (op == "[") {
                        code.push(OP_DUP1);
                        code.push(OP_MLOAD);

                        labels.push(CodeLabel({bytecodeOffset: code.length+1, dstBlock: bb.dst1}));
                        code.push(OP_PUSH4); code.push(0); code.push(0); code.push(0); code.push(0);
                        code.push(OP_JUMPI);

                        labels.push(CodeLabel({bytecodeOffset: code.length+1, dstBlock: bb.dst2}));
                        code.push(OP_PUSH4); code.push(0); code.push(0); code.push(0); code.push(0);
                        code.push(OP_JUMP);
                    } else if (op == "]") {
                        labels.push(CodeLabel({bytecodeOffset: code.length+1, dstBlock: bb.dst1}));
                        code.push(OP_PUSH4); code.push(0); code.push(0); code.push(0); code.push(0);
                        code.push(OP_JUMP);

                    // Pseudo-ops
                    } else if (op == "R") {
                        uint n = 32 * ((uint16(uint8(program[j+1])) << 8) | (uint16(uint8(program[j+2]))));
                        code.push(OP_PUSH2); code.push(uint8(n >> 8)); code.push(uint8(n));
                        code.push(OP_ADD);
                        j += 2;
                    } else if (op == "L") {
                        uint n = 32 * ((uint16(uint8(program[j+1])) << 8) | (uint16(uint8(program[j+2]))));
                        code.push(OP_PUSH2); code.push(uint8(n >> 8)); code.push(uint8(n));
                        code.push(OP_SWAP1);
                        code.push(OP_SUB);
                        j += 2;
                    } else if (op == "A") {
                        code.push(OP_DUP1);
                        code.push(OP_MLOAD);
                        code.push(OP_PUSH2); code.push(uint8(program[j+1])); code.push(uint8(program[j+2]));
                        code.push(OP_ADD);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);
                        j += 2;
                    } else if (op == "S") {
                        code.push(OP_DUP1);
                        code.push(OP_MLOAD);
                        code.push(OP_PUSH2); code.push(uint8(program[j+1])); code.push(uint8(program[j+2]));
                        code.push(OP_SWAP1);
                        code.push(OP_SUB);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);
                        j += 2;
                    } else if (op == "0") {
                        code.push(OP_PUSH1); code.push(0);
                        code.push(OP_DUP2);
                        code.push(OP_MSTORE);

                    } else if (op == "#") {
                        // no-op
                        code.push(OP_JUMPDEST);
                    } else {
                        // invalid op
                        code.push(0xde);
                        code.push(0xad);
                        code.push(uint8(op));
                        code.push(0xbe);
                        code.push(0xef);
                    }
                }
            }
            basicBlockAddrs[program.length] = code.length - constructorCodeSize;
            code.push(OP_JUMPDEST);
            code.push(OP_STOP);
            delete blocks;

            // Pass 2. Linking and assembling of labels

            for (uint i = 0; i < labels.length; i++) {
                uint p = labels[i].bytecodeOffset;
                uint dst = basicBlockAddrs[labels[i].dstBlock];
                if (dst == 0) revert("invalid code");
                code[p+0] = uint8(dst >> 24);
                code[p+1] = uint8(dst >> 16);
                code[p+2] = uint8(dst >> 8);
                code[p+3] = uint8(dst >> 0);
            }
            delete labels;
        }

        // Emit and call code
        {
            uint len = code.length - constructorCodeSize;
            code[1] = uint8(len >> 24);
            code[2] = uint8(len >> 16);
            code[3] = uint8(len >> 8);
            code[4] = uint8(len >> 0);

            bytes memory codeM = new bytes(code.length);
            for (uint i = 0; i < code.length; i++) {
                codeM[i] = bytes1(code[i]);
            }
            delete code;

            address c;
            assembly {
                c := create(0, add(codeM, 32), mload(codeM))
            }
            (bool success, bytes memory result) = c.delegatecall(stdin);
            if (!success) {
                revert("call failed");
            }
        }
    }

    // I can receive money. But how to get it out?
    receive() external payable {}
}

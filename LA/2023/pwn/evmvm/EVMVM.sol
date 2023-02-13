// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

// YES I FINALLY GOT MY METAMETAVERSE TO WORK - Arc'blroth
contract EVMVM {
    uint[] private stack;

    // executes a single opcode on the metametaverse™
    // TODO(arc) implement the last few opcodes
    function enterTheMetametaverse(bytes32 opcode, bytes32 arg) external {
        assembly {
            // declare yul bindings for the stack
            // apparently you can only call yul functions from yul :sob:
            // https://ethereum.stackexchange.com/questions/126609/calling-functions-using-inline-assembly-yul

            function spush(data) {
                let index := sload(0x00)
                let stackSlot := 0x00
                sstore(add(keccak256(stackSlot, 0x20), index), data)
                sstore(0x00, add(index, 1))
            }

            function spop() -> out {
                let index := sub(sload(0x00), 1)
                let stackSlot := 0x00
                out := sload(add(keccak256(stackSlot, 0x20), index))
                sstore(add(keccak256(stackSlot, 0x20), index), 0) // zero out the popped memory
                sstore(0x00, index)
            }

            // opcode reference: https://www.evm.codes/?fork=merge
            switch opcode
                case 0x00 { // STOP
                    // lmfao you literally just wasted gas
                }
                case 0x01 { // ADD
                    spush(add(spop(), spop()))
                }
                case 0x02 { // MUL
                    spush(mul(spop(), spop()))
                }
                case 0x03 { // SUB
                    spush(sub(spop(), spop()))
                }
                case 0x04 { // DIV
                    spush(div(spop(), spop()))
                }
                case 0x05 { // SDIV
                    spush(sdiv(spop(), spop()))
                }
                case 0x06 { // MOD
                    spush(mod(spop(), spop()))
                }
                case 0x07 { // SMOD
                    spush(smod(spop(), spop()))
                }
                case 0x08 { // ADDMOD
                    spush(addmod(spop(), spop(), spop()))
                }
                case 0x09 { // MULMOD
                    spush(mulmod(spop(), spop(), spop()))
                }
                case 0x0A { // EXP
                    spush(exp(spop(), spop()))
                }
                case 0x0B { // SIGNEXTEND
                    spush(signextend(spop(), spop()))
                }
                case 0x10 { // LT
                    spush(lt(spop(), spop()))
                }
                case 0x11 { // GT
                    spush(gt(spop(), spop()))
                }
                case 0x12 { // SLT
                    spush(slt(spop(), spop()))
                }
                case 0x13 { // SGT
                    spush(sgt(spop(), spop()))
                }
                case 0x14 { // EQ
                    spush(eq(spop(), spop()))
                }
                case 0x15 { // ISZERO
                    spush(iszero(spop()))
                }
                case 0x16 { // AND
                    spush(and(spop(), spop()))
                }
                case 0x17 { // OR
                    spush(or(spop(), spop()))
                }
                case 0x18 { // XOR
                    spush(xor(spop(), spop()))
                }
                case 0x19 { // NOT
                    spush(not(spop()))
                }
                case 0x1A { // BYTE
                    spush(byte(spop(), spop()))
                }
                case 0x1B { // SHL
                    spush(shl(spop(), spop()))
                }
                case 0x1C { // SHR
                    spush(shr(spop(), spop()))
                }
                case 0x1D { // SAR
                    spush(sar(spop(), spop()))
                }
                case 0x20 { // SHA3
                    spush(keccak256(spop(), spop()))
                }
                case 0x30 { // ADDRESS
                    spush(address())
                }
                case 0x31 { // BALANCE
                    spush(balance(spop()))
                }
                case 0x32 { // ORIGIN
                    spush(origin())
                }
                case 0x33 { // CALLER
                    spush(caller())
                }
                case 0x34 { // CALLVALUE
                    spush(callvalue())
                }
                case 0x35 { // CALLDATALOAD
                    spush(calldataload(spop()))
                }
                case 0x36 { // CALLDATASIZE
                    spush(calldatasize())
                }
                case 0x37 { // CALLDATACOPY
                    calldatacopy(spop(), spop(), spop())
                }
                case 0x38 { // CODESIZE
                    spush(codesize())
                }
                case 0x3A { // GASPRICE
                    spush(gasprice())
                }
                case 0x3B { // EXTCODESIZE
                    spush(extcodesize(spop()))
                }
                case 0x3C { // EXTCODECOPY
                    extcodecopy(spop(), spop(), spop(), spop())
                }
                case 0x3D { // RETURNDATASIZE
                    spush(returndatasize())
                }
                case 0x3E { // RETURNDATACOPY
                    returndatacopy(spop(), spop(), spop())
                }
                case 0x3F { // EXTCODEHASH
                    spush(extcodehash(spop()))
                }
                case 0x40 { // BLOCKHASH
                    spush(blockhash(spop()))
                }
                case 0x41 { // COINBASE (sponsored opcode)
                    spush(coinbase())
                }
                case 0x42 { // TIMESTAMP
                    spush(timestamp())
                }
                case 0x43 { // NUMBER
                    spush(number())
                }
                case 0x44 { // PREVRANDAO
                    spush(difficulty())
                }
                case 0x45 { // GASLIMIT
                    spush(gaslimit())
                }
                case 0x46 { // CHAINID
                    spush(chainid())
                }
                case 0x47 { // SELBALANCE
                    spush(selfbalance())
                }
                case 0x48 { // BASEFEE
                    spush(basefee())
                }
                case 0x50 { // POP
                    pop(spop())
                }
                case 0x51 { // MLOAD
                    spush(mload(spop()))
                }
                case 0x52 { // MSTORE
                    mstore(spop(), spop())
                }
                case 0x53 { // MSTORE8
                    mstore8(spop(), spop())
                }
                case 0x54 { // SLOAD
                    spush(sload(spop()))
                }
                case 0x55 { // SSTORE
                    sstore(spop(), spop())
                }
                case 0x59 { // MSIZE
                    spush(msize())
                }
                case 0x5A { // GAS
                    spush(gas())
                }
                case 0x80 { // DUP1
                    let val := spop()
                    spush(val)
                    spush(val)
                }
                case 0x91 { // SWAP1
                    let a := spop()
                    let b := spop()
                    spush(a)
                    spush(b)
                }
                case 0xF0 { // CREATE
                    spush(create(spop(), spop(), spop()))
                }
                case 0xF1 { // CALL
                    spush(call(spop(), spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF2 { // CALLCODE
                    spush(callcode(spop(), spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF3 { // RETURN
                    return(spop(), spop())
                }
                case 0xF4 { // DELEGATECALL
                    spush(delegatecall(spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF5 { // CREATE2
                    spush(create2(spop(), spop(), spop(), spop()))
                }
                case 0xFA { // STATICCALL
                    spush(staticcall(spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xFD { // REVERT
                    revert(spop(), spop())
                }
                case 0xFE { // INVALID
                    invalid()
                }
                case 0xFF { // SELFDESTRUCT
                    selfdestruct(spop())
                }
        }
    }

    fallback() payable external {
        revert("sus");
    }

    receive() payable external {
        revert("we are a cashless institution");
    }
}

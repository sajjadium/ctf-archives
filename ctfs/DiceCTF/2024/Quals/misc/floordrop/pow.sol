// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

contract Owned {
    address payable owner;

    constructor() {
        owner = payable(msg.sender);
    }

    // Access control modifier
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
}

contract ProofOfWork is Owned {
    uint256 public currentChallenge;
    uint256 public currentBlock;

    event GotFlag(uint256 indexed nonce);

    function setChallenge(uint256 challenge) public onlyOwner {
        currentChallenge = challenge;
        currentBlock = block.number;
    }

    function expireChallenge() public onlyOwner {
        currentChallenge = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;
    }

    function solveChallenge(
        bytes calldata solution,
        uint256 solver_nonce
    ) public {
        if (currentBlock != block.number) {
            revert("Too late");
        }
        if (currentChallenge == 0) {
            revert("Challenge is not yet active");
        }
        if (
            currentChallenge ==
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ) {
            revert("Challenge has expired");
        }
        uint256 _currentChallenge = currentChallenge;
        assembly {
            // Free memory pointer
            let pointer := mload(0x40)
            let base_len := solution.length
            mstore(pointer, base_len)
            mstore(add(pointer, 0x20), 1)
            mstore(add(pointer, 0x40), 5568)
            calldatacopy(add(pointer, 0x60), solution.offset, base_len)
            mstore8(add(add(pointer, 0x60), base_len), 2)
            let exp_start := add(add(add(pointer, 0x60), base_len), 1)
            for {
                let i := 32
            } lt(i, 5568) {
                i := add(i, 32)
            } {
                mstore(
                    add(exp_start, i),
                    0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
                )
            }
            mstore(
                exp_start,
                0x1ffffffffffffffffffffffffffffffffffffffffffffffffffff
            )

            let ret := staticcall(
                gas(),
                0x05,
                pointer,
                sub(add(exp_start, 5568), pointer),
                exp_start,
                5568
            )
            if iszero(ret) {
                mstore(0, 0x1)
                revert(0, 32)
            }
            let result := mload(add(exp_start, 5536))
            let success := 0
            if eq(result, _currentChallenge) {
                for {
                    let i := 0
                } lt(i, 5536) {
                    i := add(i, 32)
                } {
                    let check := mload(add(exp_start, i))
                    if gt(check, 0) {
                        mstore(0, 0x2)
                        revert(0, 32)
                    }
                }
                success := 1
            }
            if eq(not(result), _currentChallenge) {
                for {
                    let i := 32
                } lt(i, 5536) {
                    i := add(i, 32)
                } {
                    let check := mload(add(exp_start, i))
                    if gt(add(check, 1), 0) {
                        mstore(0, 0x3)
                        revert(0, 32)
                    }
                }
                {
                    let check := mload(exp_start)
                    if iszero(
                        eq(
                            check,
                            0x1ffffffffffffffffffffffffffffffffffffffffffffffffffff
                        )
                    ) {
                        mstore(0, 0x4)
                        revert(0, 32)
                    }
                }
                success := 1
            }
            if iszero(success) {
                mstore(0, 0x5)
                revert(0, 32)
            }
        }
        emit GotFlag(solver_nonce);
    }
}

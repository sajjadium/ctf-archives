// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.16;


contract Chal {
    bool public solved = false;

    constructor() payable {}

    function guess(uint _guess) public {
        uint answer = uint(
            keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))
        );

        require(answer == _guess, "Incorrect! Try again!");
        solved = true;
    }
}


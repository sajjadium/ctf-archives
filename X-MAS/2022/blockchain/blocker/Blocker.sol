// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.17;

contract Blocker {

    bool public solved = false;
    uint256 public current_timestamp;

    function _getPreviousTimestamp() internal returns (uint256) {  
        current_timestamp = block.timestamp;
        return block.timestamp;
    }
    
    function solve(uint256 _guess) public {
        require(_guess == _getPreviousTimestamp());
        solved = true;
    }
}
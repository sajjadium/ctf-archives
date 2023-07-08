pragma solidity ^0.8.13;

import "./Deception.sol";

contract Setup {
    deception public immutable TARGET;

    constructor() payable {
        TARGET = new deception(); 
    }

    function isSolved() public view returns (bool) {
        return TARGET.solved();
    }
}

pragma solidity =0.7.6;

import "./Positive.sol";

contract Setup {
    Positive public immutable TARGET;

    constructor() payable {
        TARGET = new Positive(); 
    }

    function isSolved() public view returns (bool) {
        return TARGET.solved();
    }
}

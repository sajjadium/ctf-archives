pragma solidity 0.8.16;

import "./Chal.sol";

contract Setup {
    
    Chal public immutable challenge;

    constructor() {
        challenge = new Chal();
    }
    
    function isSolved() public view returns (bool) {
        return challenge.solved();
    }
}

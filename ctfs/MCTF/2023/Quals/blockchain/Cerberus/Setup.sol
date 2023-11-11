// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.21;

import "./Cerberus.sol";

contract Setup {
    
    Cerberus public immutable challenge;

    constructor(
                bytes32 password, 
                bytes12 secretKey1, 
                uint152 secretKey2, 
                bool secretKey3
                ) 
    {
        challenge = new Cerberus(password, secretKey1, secretKey2, secretKey3);
    }
    
    function isSolved() public view returns (bool) {
        return challenge.solved();
    }
}

pragma solidity 0.7.0;

import "./DestroyMe.sol";

contract Setup {
    DestroyMe public destroyme;
    
    constructor() {
        destroyme = new DestroyMe();
    }
    
    function isSolved() public view returns (bool) {
        uint size;
        assembly {
            size := extcodesize(sload(destroyme.slot))
        }
        return size == 0;
    }
}
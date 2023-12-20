pragma solidity ^0.8.13;

import "./Chal.sol";

contract Setup {
    Chal public immutable target;

    constructor() payable {
        target = new Chal();
    }


    function isSolved() public view returns (bool) {
        if((target.dealer_tokens()==0) && (target.player_tokens()>0)){
            return true;
        }
        return false;
    }
}
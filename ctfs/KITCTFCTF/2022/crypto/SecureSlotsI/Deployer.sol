pragma solidity ^0.8.0;

import "./KAsinoChips.sol";
import "./SecureSlot.sol";

contract Deployer {
    KAsinoChips public token;
    SecureSlot public slot;

    constructor () {
        uint256 jackpot = 100_000_000;

        token = new KAsinoChips(jackpot);
        slot = new SecureSlot(token);

        token.transfer(address(slot), jackpot);
    }

    function isSolved() public view returns (bool) {
        return token.balanceOf(address(slot)) == 0;
    }
}

pragma solidity ^0.8.17;

import "./BabyWallet.sol";

contract Setup {
    BabyWallet public wallet;

    constructor() payable {
        require(msg.value == 100 ether, "requires 100 ether");
        wallet = new BabyWallet();
        payable(address(wallet)).transfer(msg.value);
    }

    function isSolved() public view returns (bool) {
        return address(wallet).balance == 0 ether;
    }
}
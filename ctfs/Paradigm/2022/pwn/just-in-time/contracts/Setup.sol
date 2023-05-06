pragma solidity ^0.8.13;

import "./JIT.sol";

contract Setup {
    JIT public immutable TARGET;

    constructor() payable {
        require(msg.value == 50 ether);

        TARGET = new JIT();

        payable(address(TARGET)).transfer(msg.value);
    }

    function isSolved() external view returns (bool) {
        return address(TARGET).balance == 0;
    }
}
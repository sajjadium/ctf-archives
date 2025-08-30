// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        require(msg.value > 0, "no value");
        balances[msg.sender] += msg.value;
    }

    function withdrawAll() external {
        uint256 bal = balances[msg.sender];
        require(bal > 0, "no balance");

        (bool ok, ) = msg.sender.call{value: bal}("");
        require(ok, "send failed");

        balances[msg.sender] = 0;
    }

    receive() external payable {}
}

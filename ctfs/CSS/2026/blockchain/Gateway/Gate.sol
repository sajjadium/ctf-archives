// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title Gate — three doors stand between you and the flag.
contract Gate {
    address public owner;      // slot 0
    bytes32 private password;  // slot 1
    bool private stepped;      // slot 2
    bool private funded;       // slot 3
    bool public solved;        // slot 4

    constructor() payable {
        owner = msg.sender;
        password = keccak256(abi.encodePacked("gateway to the flag"));
    }

    /// @notice Door 1: only a contract may pass.
    function enter() external {
        require(tx.origin != msg.sender, "Gate: must be called from a contract");
        stepped = true;
    }

    /// @notice Door 2: pay homage in plain ether.
    receive() external payable {
        require(stepped, "Gate: complete door 1 first");
        require(msg.value > 0, "Gate: send some ether");
        funded = true;
    }

    /// @notice Door 3: speak the password.
    function claim(bytes32 _password) external {
        require(stepped, "Gate: complete door 1 first");
        require(funded, "Gate: complete door 2 first");
        require(_password == password, "Gate: wrong password");
        solved = true;
    }
}

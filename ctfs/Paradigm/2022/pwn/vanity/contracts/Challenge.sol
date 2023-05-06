// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.7.6;

import "./SignatureChecker.sol";

contract Challenge {
    bytes32 private immutable MAGIC = keccak256(abi.encodePacked("CHALLENGE_MAGIC"));

    uint public bestScore;

    function solve() external {
        solve(msg.sender);
    }

    function solve(address signer, bytes memory signature) external {
        require(SignatureChecker.isValidSignatureNow(signer, MAGIC, signature), "Challenge/invalidSignature");

        solve(signer);
    }

    function solve(address who) private {
        uint score = 0;

        for (uint i = 0; i < 20; i++) if (bytes20(who)[i] == 0) score++;

        if (score > bestScore) bestScore = score;
    }
}
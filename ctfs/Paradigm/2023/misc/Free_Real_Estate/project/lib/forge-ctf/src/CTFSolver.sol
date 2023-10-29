// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.6.2 <0.9.0;

import "forge-std/Script.sol";

abstract contract CTFSolver is Script {
    function run() external {
        uint256 playerPrivateKey = vm.envOr("PLAYER", uint256(0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80));
        address challenge = vm.envAddress("CHALLENGE");

        vm.startBroadcast(playerPrivateKey);

        solve(challenge, vm.addr(playerPrivateKey));

        vm.stopBroadcast();
    }

    function solve(address challenge, address player) virtual internal;
}
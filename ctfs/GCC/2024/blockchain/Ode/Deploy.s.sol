// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {Challenge} from "../src/Challenge.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    Challenge public challenge;
    
    function run() public {
        vm.startBroadcast();

        challenge = new Challenge();
        console.log("Challenge deployed at :", address(challenge));

        vm.stopBroadcast();
    }
}

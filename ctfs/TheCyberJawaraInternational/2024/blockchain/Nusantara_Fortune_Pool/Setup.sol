// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./NusantaraFortuneOperator.sol";

contract Setup {
    NusantaraFortuneOperator public operator;
    address public poolA;
    address public poolB;
    address public poolC;
    address public poolD;
    address public poolE;
    address public poolF;
    bytes32[6] public poolIds;

    constructor() payable {
        operator = new NusantaraFortuneOperator();

        address[6] memory poolAddresses;

        for (uint i = 0; i < 5; i++) {
            (poolIds[i], poolAddresses[i]) = operator.deployNewPool(i);
        }

        poolA = poolAddresses[0];
        poolB = poolAddresses[1];
        poolC = poolAddresses[2];
        poolD = poolAddresses[3];
        poolE = poolAddresses[4];

        // Deploy and activate the sixth pool
        (poolIds[5], poolF) = operator.deployNewPool(4);
        operator.activatePool(poolIds[5], poolF);
        operator.verifyPool(poolIds[5], poolF);
        operator.contributeToPool{value: 44 ether}(poolIds[5], poolF);
    }

    function activatePool(uint256 poolIndex) external payable {
        require(poolIndex < 5, "Invalid pool index");
        address pool = [poolA, poolB, poolC, poolD, poolE][poolIndex];
        require(msg.value == poolIndex*0.01 ether, "Incorrect activation fee");
        operator.activatePool(poolIds[poolIndex], pool);
        operator.verifyPool(poolIds[poolIndex], pool);
    }

    function isSolved() external view returns (bool) {
        return address(operator).balance == 0;
    }
}
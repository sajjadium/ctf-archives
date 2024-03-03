// SPDX-License-Identifier: MIT
pragma solidity 0.8.23;

import "./Cubes.sol";

contract Challenge {
    CubeFactory public target;
    address constant PLAYER = 0xCaffE305b3Cc9A39028393D3F338f2a70966Cb85;

    constructor() payable{
        target = new CubeFactory();

        target.createCube{value : 1 ether}(25655478,65516125,5981561545,1337);
        target.createCube{value : 1 ether}(98981916,51891651,1984651616,5555);
    }


    function isSolved() external returns (bool solved) {

        return PLAYER.balance > 10_000 ether;
    }
}
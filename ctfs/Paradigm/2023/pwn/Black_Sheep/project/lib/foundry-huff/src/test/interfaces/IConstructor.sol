// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

interface IConstructor {
    function getArgOne() external returns (address);
    function getArgTwo() external returns (uint256);
}

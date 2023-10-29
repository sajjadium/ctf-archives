// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

interface INumber {
    function setNumber(uint256) external;
    function getNumber() external returns (uint256);
}

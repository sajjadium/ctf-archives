// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

interface IPigeonVaultFacet {
    function emergencyWithdraw() external;
    function contractBalance() external view returns (uint256);
    function getContractAddress() external view returns (address);
}

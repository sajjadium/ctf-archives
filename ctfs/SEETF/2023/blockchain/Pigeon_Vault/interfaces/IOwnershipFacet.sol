// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

interface IOwnershipFacet {
    function owner() external view returns (address);
    function transferOwnership(address _newOwner) external;
}

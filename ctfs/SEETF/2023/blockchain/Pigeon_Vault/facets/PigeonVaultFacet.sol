// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage} from "../libraries/LibAppStorage.sol";
import {LibDiamond} from "../libraries/LibDiamond.sol";

contract PigeonVaultFacet {
    AppStorage internal s;

    event Deposit(address indexed account, uint256 amount);

    function emergencyWithdraw() public {
        LibDiamond.enforceIsContractOwner();
        address owner = LibDiamond.contractOwner();
        (bool success,) = payable(address(owner)).call{value: address(this).balance}("");
        require(success, "PigeonVaultFacet: emergency withdraw failed");
    }

    function contractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function getContractAddress() external view returns (address) {
        return address(this);
    }

    // receive() external payable {
    //     emit Deposit(msg.sender, msg.value);
    // }
}

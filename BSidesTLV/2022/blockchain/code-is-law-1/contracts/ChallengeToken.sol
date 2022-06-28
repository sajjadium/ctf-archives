//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "hardhat/console.sol";

contract ChallengeToken is ERC20 {
    bytes32 private onlyICanHazTokenContractCodeHash =
        0x1431A52467B8E0B496D710A30B897A6EB093CD9137FBF9B34B47441FD5E868F3;

    constructor() ERC20("ChallengeToken", "BSIDES2022") {}

    function did_i_win() public view returns (string memory) {
        if (balanceOf(msg.sender) == 0) {
            revert("you shall not pass");
        }

        return "BSidesTLV2022{PLACEHOLDER}";
    }

    function can_i_haz_token(address receiver) public {
        require(
            receiver == calculateAddressOfTheFirstContractDeployedBy(tx.origin),
            "receiver is ineligible for a token because they are not the first contract deployed by the EOA who initiated this transaction"
        );
        require(
            getContractCodeHash(receiver) == onlyICanHazTokenContractCodeHash,
            "receiver is ineligible for a token because their codehash does not match the specific contract codehash required"
        );

        if (balanceOf(receiver) == 0) {
            _mint(receiver, 1);
        }
    }

    function getContractCodeHash(address contractAddress)
        private
        view
        returns (bytes32 callerContractCodeHash)
    {
        assembly {
            callerContractCodeHash := extcodehash(contractAddress)
        }
    }

    // Copied from https://ethereum.stackexchange.com/a/87840
    function calculateAddressOfTheFirstContractDeployedBy(address deployer)
        private
        pure
        returns (address _address)
    {
        bytes32 hash = keccak256(
            abi.encodePacked(bytes1(0xd6), bytes1(0x94), deployer, bytes1(0x80))
        );

        assembly {
            mstore(0, hash)
            _address := mload(0)
        }
    }
}

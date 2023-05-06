// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @title Secret And Ephemeral
 * @author Blue Alder (https://duc.tf)
 **/

contract SecretAndEphemeral {
    address private owner;
    int256 public seconds_in_a_year = 60 * 60 * 24 * 365;
    string word_describing_ductf = "epic";
    string private not_yours;
    mapping(address => uint) public cool_wallet_addresses;

    bytes32 public spooky_hash; //

    constructor(string memory _not_yours, uint256 _secret_number) {
        not_yours = _not_yours;
        spooky_hash = keccak256(abi.encodePacked(not_yours, _secret_number, msg.sender));
    }

    function giveTheFunds() payable public {
        require(msg.value > 0.1 ether);
        // Thankyou for your donation
        cool_wallet_addresses[msg.sender] += msg.value;
    }

    function retrieveTheFunds(string memory secret, uint256 secret_number, address _owner_address) public {
        bytes32 userHash = keccak256(abi.encodePacked(secret, secret_number, _owner_address));

        require(userHash == spooky_hash, "Somethings wrong :(");

        // User authenticated, sending funds
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }
}
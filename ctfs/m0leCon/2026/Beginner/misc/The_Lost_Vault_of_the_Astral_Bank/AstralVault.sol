// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// From: https://github.com/OpenZeppelin/openzeppelin-contracts
import "openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol";
import "openzeppelin-contracts/contracts/utils/cryptography/MessageHashUtils.sol";

contract AstralVault {
    using ECDSA for bytes32;

    address public backendSigner;

    mapping(address => uint256) public balances;
    mapping(bytes32 => bool) public usedHashes; // prevent replay

    constructor(address _backendSigner) {
        backendSigner = _backendSigner;
    }

    function donate(
        address recipient,
        uint256 createdAt,
        uint256 expiresAt,
        bytes calldata signature
    ) public payable {
        require(
            block.timestamp >= createdAt && block.timestamp <= expiresAt,
            "Deposit signature not valid in this time frame"
        );

        bytes32 hash = keccak256(
            abi.encodePacked(
                msg.sender,
                recipient,
                msg.value,
                createdAt,
                expiresAt
            )
        );

        bytes32 ethHash = MessageHashUtils.toEthSignedMessageHash(hash);

        require(!usedHashes[ethHash], "Signature already used");
        usedHashes[ethHash] = true;

        address recovered = ethHash.recover(signature);
        require(recovered == backendSigner, "Invalid deposit signature");

        balances[recipient] += msg.value;
    }

    function balanceOf(address _who) public view returns (uint256 balance) {
        return balances[_who];
    }

    function withdraw(uint256 _amount) public {
        unchecked {
            if (balances[msg.sender] >= _amount) {
                (bool result, ) = msg.sender.call{value: _amount}("");
                if (result) {
                    _amount;
                }
                balances[msg.sender] -= _amount;
            }
        }
    }

    receive() external payable {}
}

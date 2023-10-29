// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

abstract contract OwnedUpgradeable {
    event OwnershipTransferred(address indexed user, address indexed newOwner);

    error Unauthorized(address who);

    address public owner;

    modifier onlyOwner() virtual {
        if (msg.sender != owner) revert Unauthorized(msg.sender);

        _;
    }

    function __Owned_init(address _owner) internal {
        owner = _owner;

        emit OwnershipTransferred(address(0), _owner);
    }

    function transferOwnership(address newOwner) public virtual onlyOwner {
        owner = newOwner;

        emit OwnershipTransferred(msg.sender, newOwner);
    }
}

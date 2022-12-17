
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

abstract contract BucketsBase {
    uint256[] public buckets;
}

contract Buckets is BucketsBase, Initializable, ERC20 {
    uint256 private constant MAX_BUCKETS = 10;

    constructor() ERC20("Buckets", "Bucket") {}

    function initialize(uint256 premint) external initializer {
        buckets = new uint256[](MAX_BUCKETS);

        buckets[0] = premint;
        _mint(msg.sender, premint);
    }

    // put some ether in a bucket and mint bucket tokens
    function deposit(uint256 bucketNumber, uint256 value) external payable {
        buckets[bucketNumber] += value;
        _mint(msg.sender, value);
    }

    // withdraw some ether from a bucket and burn bucket tokens
    function withdraw(uint256 bucketNumber, uint256 amount) external {
        buckets[bucketNumber] -= amount;
        _burn(msg.sender, amount);
    }
}
// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

import "./MerkleDistributor.sol";

contract Token is ERC20Like {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    uint256 public totalSupply = 1_000_000 ether;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }

    function approve(address to, uint256 amount) public returns (bool) {
        allowance[msg.sender][to] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        return transferFrom(msg.sender, to, amount);
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        if (from != msg.sender) {
            allowance[from][to] -= amount;
        }
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

contract Setup {

    Token public immutable token;
    MerkleDistributor public immutable merkleDistributor;

    constructor() payable {
        token = new Token();
        uint256 airdropAmount = 75000 * 10 ** 18;
        merkleDistributor = new MerkleDistributor(
            address(token), 
            bytes32(0x5176d84267cd453dad23d8f698d704fc7b7ee6283b5131cb3de77e58eb9c3ec3)
        );
        token.transfer(address(merkleDistributor), airdropAmount);
    }

    function isSolved() public view returns (bool) {
        bool condition1 = token.balanceOf(address(merkleDistributor)) == 0;
        bool condition2 = false;
        for (uint256 i = 0; i < 64; ++i) {
            if (!merkleDistributor.isClaimed(i)) {
                condition2 = true;
                break;
            }
        }
        return condition1 && condition2;
    }
}
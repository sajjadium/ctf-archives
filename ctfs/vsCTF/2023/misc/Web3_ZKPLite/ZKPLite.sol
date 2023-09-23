//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

pragma abicoder v2;

library ZKPLiteLib {
    struct Proof {
        uint256 a;
        uint256 b;
        uint256 c;
    }

    function hash(Proof memory proof) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(proof.a, proof.b, proof.c));
    }

    function verifyProof(Proof memory proof, address from, address to, uint256 amount) internal view returns (bool) {
        uint256 challenge = uint256(keccak256(abi.encodePacked(from, to, amount))) % 2**32;
        uint256 sum = proof.a + proof.b;

        uint256 hashed_sender_relation = uint256(keccak256(abi.encodePacked(msg.sender, proof.a))) % 2**32;

        return (sum == amount)
            && (challenge * proof.a % 2**128 == proof.c)
            && (proof.a * proof.b % 2**128 == proof.c)
            && (hashed_sender_relation == proof.b);
    }
}

contract ZKPLite {
    using ZKPLiteLib for ZKPLiteLib.Proof;

    uint256 private constant TOKEN_SUPPLY = 133337;
    address owner;
    mapping(address => uint256) private balances;
    mapping(bytes32 => bool) private usedProofs;

    constructor()  {
        balances[msg.sender] = TOKEN_SUPPLY;
        owner = msg.sender;
    }

    function transfer(address to, uint256 amount, ZKPLiteLib.Proof memory proof) public {
        require(amount <= balances[owner], "Insufficient offer");
        require(!usedProofs[proof.hash()], "Proof already used");
        require(ZKPLiteLib.verifyProof(proof, msg.sender, to, amount), "Invalid proof");

        usedProofs[proof.hash()] = true;
        balances[owner] -= amount;
        balances[to] += amount;
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function isSolved() public view returns (bool) {
        return balances[owner] == 0;
    }
}

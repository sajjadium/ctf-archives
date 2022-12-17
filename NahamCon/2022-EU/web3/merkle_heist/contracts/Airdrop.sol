// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
interface ISimpleToken {
    function mint(address addr, uint256 amount) external;
}

contract Airdrop {

    ISimpleToken public immutable token;
    mapping(address => bool) public dropped;

    // merkle tree
    bytes32 immutable merkleRoot;
    uint256 immutable proofLength;
    uint256 immutable dropPerAddress;

    bytes32[] _latestAcceptedProof;

    constructor(
        ISimpleToken _token,
        uint256 _dropPerAddress,
        bytes32 _merkleRoot,
        uint256 _proofLength
    ) {
        require(address(_token) != address(0), "Token address cannot be zero");
        require(uint256(_merkleRoot) != 0, "Merkle root cannot be zero");
        require(_proofLength > 2, "Merkle proof cannot be this short");
        require(_dropPerAddress > 0, "Airdrop should be positive");

        token = _token;
        proofLength = _proofLength;
        merkleRoot = _merkleRoot;
        dropPerAddress = _dropPerAddress;
    }

    function mintToken(bytes32[] memory merkleProof) external {
        require(!dropped[msg.sender], "Already dropped");
        require(merkleProof.length == proofLength, "Tree length mismatch");
        require(address(uint160(uint256(merkleProof[0]))) == msg.sender, "First Merkle leaf should be the msg.sender's address");
        require(proofHash(merkleProof) == merkleRoot, "Merkle proof failed");

        dropped[msg.sender] = true;
        token.mint(msg.sender, dropPerAddress);
        _latestAcceptedProof = merkleProof;
    }

    function latestAcceptedProof() public view returns (bytes32[] memory) {
        return _latestAcceptedProof;
    }


    function proofHash(bytes32[] memory nodes) internal pure returns (bytes32 result) {
        result = pairHash(nodes[0], nodes[1]);
        for (uint256 i = 2; i < nodes.length; i++) {
            result = pairHash(result, nodes[i]);
        }
    }

    function pairHash(bytes32 a, bytes32 b) internal pure returns (bytes32) {
        return keccak256(abi.encode(a ^ b));
    }
}

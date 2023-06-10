// SPDX-License-Identifier: Unlicense

pragma solidity ^0.8.0;

library MerkleProof {
    // Verify a Merkle proof proving the existence of a leaf in a Merkle tree. Assumes that each pair of leaves and each pair of pre-images in the proof are sorted.
    function verify(bytes32[] calldata proof, bytes32 root, uint256 index) internal pure returns (bool) {
        bytes32 computedHash = bytes32(abi.encodePacked(index));

        require(root != bytes32(0), "MerkleProof: Root hash cannot be zero");
        require(computedHash != bytes32(0), "MerkleProof: Leaf hash cannot be zero");

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (computedHash < proofElement) {
                // Hash(current computed hash + current element of the proof)
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                // Hash(current element of the proof + current computed hash)
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        // Check if the computed hash (root) is equal to the provided root
        return computedHash == root;
    }
}

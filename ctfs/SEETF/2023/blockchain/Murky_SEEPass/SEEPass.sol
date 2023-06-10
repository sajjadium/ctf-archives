// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "./MerkleProof.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SEEPass is ERC721 {
    bytes32 private _merkleRoot;
    mapping(uint256 => bool) private _minted;

    constructor(bytes32 _root) ERC721("SEE Pass", "SEEP") {
        _merkleRoot = _root;
    }

    function mintSeePass(bytes32[] calldata _proof, uint256 _tokenId) public {
        require(!hasMinted(_tokenId), "Already minted");
        require(verify(_proof, _merkleRoot, _tokenId), "Invalid proof");

        _minted[_tokenId] = true;

        _safeMint(msg.sender, _tokenId);
    }

    function verify(bytes32[] calldata proof, bytes32 root, uint256 index) public pure returns (bool) {
        return MerkleProof.verify(proof, root, index);
    }

    function hasMinted(uint256 _tokenId) public view returns (bool) {
        return _minted[_tokenId];
    }
}

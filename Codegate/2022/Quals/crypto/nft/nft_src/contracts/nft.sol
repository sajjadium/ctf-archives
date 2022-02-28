// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;


import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/utils/Counters.sol";

contract PrivateNFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    using Strings for uint256;
    mapping(uint256 => string) private _tokenURIs;
    mapping(address => uint256[]) private _tokenIDs;

    constructor() ERC721("CodeGate", "CDG") {}

    function getTokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId));
        require(ownerOf(tokenId) == msg.sender);

        string memory _tokenURI = _tokenURIs[tokenId];
        string memory base = _baseURI();

        if (bytes(base).length == 0) {
            return _tokenURI;
        }
        if (bytes(_tokenURI).length > 0) {
            return string(abi.encodePacked(base, _tokenURI));
        }

        return super.tokenURI(tokenId);
    }

    function getIDs() public view returns (uint256[] memory) {
        return _tokenIDs[msg.sender];
    }

    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal {
        require(_exists(tokenId));
        _tokenURIs[tokenId] = _tokenURI;
    }

    modifier contains (string memory what, string memory where) {
        bytes memory whatBytes = bytes (what);
        bytes memory whereBytes = bytes (where);
    
        require(whereBytes.length >= whatBytes.length);
    
        bool found = false;
        for (uint i = 0; i <= whereBytes.length - whatBytes.length; i++) {
            bool flag = true;
            for (uint j = 0; j < whatBytes.length; j++)
                if (whereBytes [i + j] != whatBytes [j]) {
                    flag = false;
                    break;
                }
            if (flag) {
                found = true;
                break;
            }
        }
        require (!found);
    
        _;
    }

    function mintNft(string memory tokenURI) external contains ("127.0.0.1", tokenURI) contains ("0.0.0.0", tokenURI) returns (uint256) {
        require(balanceOf(msg.sender) <= 3);
        _tokenIds.increment();

        uint256 newNftTokenId = _tokenIds.current();
        _mint(msg.sender, newNftTokenId);
        _setTokenURI(newNftTokenId, tokenURI);
        _tokenIDs[msg.sender].push(newNftTokenId);
        return newNftTokenId;
    }
}

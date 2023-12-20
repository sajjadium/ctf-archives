// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Vuln is ERC721, Ownable {
    uint256 constant public COST = 0.69 ether;
    uint16 constant public CAP = 42000;
    uint8 constant public CAN = 10;

    uint16 public CURRENT;
    mapping(address => uint8) public COUNT;

    constructor(address initialOwner) ERC721("Back Door", "BD") Ownable(initialOwner) {}

    event MintFailed(string reason);
    error InvalidMintAmount();
    error ExceededCap();
    error NotEnoughETH();
    error ExceededCAN();
  
    function mint(uint8 _mintAmount) external payable {
        if (_mintAmount == 0 || _mintAmount > CAN) {
            emit MintFailed("wrong _mintAmount");
            revert InvalidMintAmount();
        }
    
        if (CURRENT + _mintAmount > CAP) {
            emit MintFailed("Exceeded Cap");
            revert ExceededCap();
        }

        if (msg.value != COST * _mintAmount) {
            emit MintFailed("not enough ETH");
            revert NotEnoughETH();
        }
    
        if (COUNT[msg.sender] + _mintAmount > CAN) {
            emit MintFailed("exceeded CAN");
            revert ExceededCAN();
        }

        payable(owner()).call{value: msg.value}("");
        COUNT[msg.sender] += _mintAmount;

        for (uint8 i = 1; i <= _mintAmount; i++) {
            CURRENT += 1;
            _safeMint(msg.sender, CURRENT);
        }
    }

    event BurnFailed(string reason);

    function burn(uint16 SECRET_KEY) external {
        if (SECRET_KEY == 0 || SECRET_KEY > CURRENT) {
            emit BurnFailed("wrong SECRET_KEY");
            revert();
        }
        if (ownerOf(SECRET_KEY) != msg.sender) {
            emit BurnFailed("not owner of the token");
            revert();
        }

        _burn(SECRET_KEY);
        CURRENT -= 1;
    }
}

contract Setup is ERC721Holder {

    Vuln public vuln;

   constructor() payable  {
       vuln = new Vuln(msg.sender);
   }
   function isSolved() public returns (bool) {
    try vuln.mint{value: 0.69 ether}(1) {
        return false;
    } catch (bytes memory reason) {
        bytes4 expectedSelector = bytes4(keccak256("ERC721InvalidSender(address)"));
        bytes4 receivedSelector;
        assembly {
            receivedSelector := mload(add(reason, 0x20))
        }
        return (expectedSelector == receivedSelector);
    }
}



    event MintFailed(string reason);

    function mintVuln() public {
        try vuln.mint{value: 0.69 ether}(1) {

        } catch Error(string memory reason) {
            emit MintFailed(reason);
        }
    }

    function burnVuln(uint16 SECRET_KEY) public {
        vuln.burn(SECRET_KEY);
    }
}

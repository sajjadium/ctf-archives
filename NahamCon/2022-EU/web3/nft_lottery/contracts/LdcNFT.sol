//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LdcNFT is ERC721Enumerable, Ownable {
  using Strings for uint256;

  string public baseURI;
  string public baseExtension = ".json";
  bool public preSaleOn = false;
  bool public publicSaleOn = false;
  bool public santaAlgorithmOn = false;
  bool public revealed = false;
  uint256 public maxSupply = 2500;
  uint256 public reserved = 100;
  uint256 public preSaleCost = 0.055 ether;
  uint256 public publicSaleCost = 0.065 ether;
  uint256 public preSaleMaxMintAmount = 3;
  uint256 public publicSaleMaxMintAmount = 6;
  uint256 public prizeAmount = 6 ether;
  uint256 public prize1ETH = 1 ether;
  uint256 public prize05ETH = 0.5 ether;
  uint256 public prize01ETH = 0.1 ether;

  mapping (address => uint256) public minted;
  mapping (address => bool) public whiteListedWallets;

  constructor(
    string memory _name,
    string memory _symbol,
    string memory _initBaseURI
  ) ERC721(_name, _symbol) {
    setBaseURI(_initBaseURI);
  }

  // internal
  function _baseURI() internal view virtual override returns (string memory) {
    return baseURI;
  }

  function mint(address _to, uint256 _mintAmount) public payable {
    bool saleOn = (preSaleOn || publicSaleOn);
    require(saleOn, "Sale must be ON");
     
    uint256 supply = totalSupply();

    if (msg.sender != owner()) {
     if (preSaleOn) {
      require(preSaleOn, "Presale must be ON");
      require(_mintAmount > 0, "Mint abmount must be more than 0");
      require(whiteListedWallets[msg.sender] == true, "You aren't whitelisted!");
      require(supply + _mintAmount <= maxSupply, "Purchase would exceed max supply of NFTs");
      require(minted[msg.sender] + _mintAmount <= preSaleMaxMintAmount, "Purchase would exceed max tokens for presale");
      require(msg.value >= preSaleCost * _mintAmount, "Ether value sent is not correct");

     } else if (publicSaleOn) {
      require(publicSaleOn, "Publicsale must be ON");
      require(_mintAmount > 0, "Mint abmount must be more than 0");
      require(supply + _mintAmount <= maxSupply - reserved, "Purchase would exceed max supply of NFTs");
      require(minted[msg.sender] + _mintAmount <= publicSaleMaxMintAmount, "Purchase would exceed max tokens for sale");
      require(msg.value >= publicSaleCost * _mintAmount, "Ether value sent is not correct");
      
      }
    }

    for (uint256 i = 1; i <= _mintAmount; i++) {
          _safeMint(_to, supply + i);
    } 

    minted[msg.sender] += _mintAmount;  

      // Santa algorithm
    if (santaAlgorithmOn && prizeAmount > 0 && msg.sender != owner()) {
      
      uint rnd = random();        
      if (rnd < 1 && address(this).balance > prize1ETH) {
        payable(_to).transfer(prize1ETH);
        prizeAmount -= prize1ETH;
      } else if (rnd < 4 && address(this).balance > prize05ETH) {
        payable(_to).transfer(prize05ETH);
        prizeAmount -= prize05ETH;
      } else if (rnd < 80 && address(this).balance > prize01ETH) {
        payable(_to).transfer(prize01ETH);
        prizeAmount -= prize01ETH;
      }
    }
   }

  function random() internal returns (uint) {
    uint randomnumber = uint(keccak256(abi.encodePacked(block.timestamp, block.difficulty, msg.sender))) % 999;
    return randomnumber;
  }

  function setPrizeAmount(uint256 _prizeAmount) public onlyOwner {
    prizeAmount = _prizeAmount;
  }
    
  function flipPublicSaleOn() public onlyOwner {
    publicSaleOn = !publicSaleOn;
  }

  function flipSantaAlgorithmOn() public onlyOwner {
    santaAlgorithmOn = !santaAlgorithmOn;
  }
  
  function setBaseURI(string memory _newBaseURI) public onlyOwner {
    baseURI = _newBaseURI;
  }
  
  receive() external payable {

  }
}

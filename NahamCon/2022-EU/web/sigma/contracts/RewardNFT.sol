// SPDX-License-Identifier: Unlicensed
// @author - Ataberk Yavuzer
pragma solidity ^0.8.0;

import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract RewardNFT is ERC721{

    uint8 public totalSupply;
    address internal escrowContract;

    modifier onlyEscrowContract{
        require(escrowContract != address(0), "RewardNFT::not initialized");
        require(msg.sender == escrowContract, "RewardNFT::only escrow contract");
        _;
    }
    constructor(address _escrowContract) ERC721("Reward NFT", "REW") {
        require(_escrowContract != address(0), "RewardNFT::zero address");
        escrowContract = _escrowContract;
    }

    function mintAsReward(address _account) external onlyEscrowContract {
        totalSupply++;
        _mint(_account, 777);
    }
}
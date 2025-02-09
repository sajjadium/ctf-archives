// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AngelInvestor {
    struct Startup {
        uint256 fundingAmount;
        uint256 equityOffered;
        bool hasReceivedFunding;
        bool isBought;
    }

    mapping(address => Startup) public startups;
    address public investor;
    uint256 public totalFunds;
    bool public challengeSolved = false;

    uint256 public constant BUYOUT_RATE = 400 ether;
    uint256 public constant CHALLENGE_THRESHOLD = 100 ether;

    modifier onlyInvestor() {
        require(msg.sender == investor, "Only investor can perform this");
        _;
    }

    constructor() payable {
        investor = msg.sender;
        totalFunds = address(this).balance;
    }

    function applyForFunding(uint256 equityOffered) external {
        require(equityOffered > 0 && equityOffered <= 7, "Equity offered must be between 1% and 7%");
        require(!startups[msg.sender].hasReceivedFunding, "Already funded");

        uint256 fundingAmount = equityOffered * 3 ether;
        require(fundingAmount <= 21 ether, "Cannot exceed 21 ETH funding");
        require(totalFunds >= fundingAmount, "Not enough funds available");

        (bool success, ) = msg.sender.call{value: fundingAmount}("");
        require(success, "Funding transfer failed");

        totalFunds -= fundingAmount;
        startups[msg.sender].fundingAmount += fundingAmount;
        startups[msg.sender].equityOffered = equityOffered;
        startups[msg.sender].hasReceivedFunding = true;
    }

    function donateToInvestorPool() external payable {
        require(msg.value > 0, "Must donate some ETH");
        totalFunds += msg.value;
    }

    function buyCompany(address startupOwner) external onlyInvestor {
        require(startups[startupOwner].hasReceivedFunding, "Startup must be funded first");
        require(!startups[startupOwner].isBought, "Company already bought");
        require(totalFunds >= BUYOUT_RATE, "Not enough funds to buy");

        (bool success, ) = startupOwner.call{value: BUYOUT_RATE}("");
        require(success, "Purchase transfer failed");

        totalFunds -= BUYOUT_RATE;
        startups[startupOwner].isBought = true;
    }

    function isChallSolved() external returns (bool) {
        if (!challengeSolved && msg.sender.balance >= CHALLENGE_THRESHOLD) {
            challengeSolved = true;
        }
        return challengeSolved;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VeHAL is ERC20 {
    uint256 public constant MAX_UINT256 = type(uint256).max;

    uint8 public _decimals; //How many decimals to show.

    mapping(address => uint256) public locked;

    bool airdropped;

    constructor(
        uint256 _initialAmount,
        string memory _tokenName,
        uint8 _decimalUnits,
        string memory _tokenSymbol
    ) ERC20(_tokenName, _tokenSymbol) {
        require(_decimalUnits == 18);

        _mint(msg.sender, _initialAmount);

        _decimals = _decimalUnits; // Amount of decimals for display purposes
    }

    address proposer;

    modifier onlyOnboardProposal() {
        require(msg.sender == proposer, "Only onboardProposal");
        _;
    }

    function setOnboardProposal(address _new) external {
        require(proposer == address(0), "Already set");
        proposer = _new;
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    // We give a 20% of the total supply to the first caller!
    // Not enought to vote for a valid proposal, as 30% is required :(
    function airdrop() external {
        require(!airdropped, "Already claimed");
        _mint(msg.sender, totalSupply() / 5);
        airdropped = true;
    }

    function lockVeHAL(address _owner, uint256 _value) public onlyOnboardProposal {
        locked[_owner] += _value;
    }

    function unlockVeHAL(address _owner, uint256 _value) public onlyOnboardProposal {
        locked[_owner] -= _value;
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override {
        if(from != address(0)){
            revert("No transfers allowed");
        }
    }

}

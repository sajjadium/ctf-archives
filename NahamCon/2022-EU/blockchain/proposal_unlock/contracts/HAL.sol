// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract HAL is ERC20 {
    uint256 public constant PROPOSE_THRESHOLD = 10000 ether;

    uint256 public constant MAX_UINT256 = type(uint256).max;

    uint8 public _decimals; //How many decimals to show

    mapping(address => bool) public alreadyMinted;

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

    /**
     * @notice This is for frontend mint
     */
    function mint() external {
        require(!alreadyMinted[msg.sender], "Already minted");
        alreadyMinted[msg.sender] = true;

        _mint(msg.sender, PROPOSE_THRESHOLD);
    }

    function burnHalborn(address _account, uint256 _amount) external onlyOnboardProposal {
        _burn(_account, _amount);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }
}

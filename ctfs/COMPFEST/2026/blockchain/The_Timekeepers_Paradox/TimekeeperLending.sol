// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./TimekeeperToken.sol";

contract TimekeeperLending {
    TimekeeperToken public token;
    address public oracle; // oracle proxy address

    uint256 public constant COLLATERAL_RATIO = 150;
    uint256 public constant RATIO_PRECISION = 100;

    uint256 public constant FLASHLOAN_FEE = 10; // basis points
    uint256 public constant FEE_PRECISION = 10000;

    struct Position {
        uint256 ethCollateral;   
        uint256 tokenDebt;       
        uint256 tokenCollateral; 
        uint256 ethDebt;         
    }

    mapping(address => Position) public positions;
    
    address public admin;
    bool private _flashloanActive;

    event ETHDeposited(address indexed user, uint256 amount);
    event ETHBorrowed(address indexed user, uint256 amount);
    event TokenDeposited(address indexed user, uint256 amount);
    event TokenBorrowed(address indexed user, uint256 amount);
    event PositionLiquidated(address indexed user, address indexed liquidator);
    event FlashloanExecuted(address indexed borrower, uint256 amount);

    constructor(address _token, address _oracle) {
        token = TimekeeperToken(_token);
        oracle = _oracle;
        admin = msg.sender;
    }

    function getOraclePrice() public view returns (uint256) {
        // Call the oracle proxy's getLatestPrice() function
        (bool success, bytes memory data) = oracle.staticcall(
            abi.encodeWithSignature("getLatestPrice()")
        );
        require(success && data.length >= 32, "Oracle call failed");
        return abi.decode(data, (uint256));
    }

    function depositETH() external payable {
        require(msg.value > 0, "Zero deposit");
        positions[msg.sender].ethCollateral += msg.value;
        emit ETHDeposited(msg.sender, msg.value);
    }

    function depositToken(uint256 amount) external {
        require(amount > 0, "Zero deposit");
        require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        positions[msg.sender].tokenCollateral += amount;
        emit TokenDeposited(msg.sender, amount);
    }

    function borrowToken(uint256 amount) external {
        uint256 price = getOraclePrice(); // TKG per ETH
        Position storage pos = positions[msg.sender];

        uint256 maxBorrow = (pos.ethCollateral * price * RATIO_PRECISION) / 
                           (COLLATERAL_RATIO * 1e18);

        require(pos.tokenDebt + amount <= maxBorrow, "Insufficient collateral");
        
        pos.tokenDebt += amount;
        token.transfer(msg.sender, amount);
        emit TokenBorrowed(msg.sender, amount);
    }

    function borrowETH(uint256 amount) external {
        uint256 price = getOraclePrice(); // TKG per ETH
        Position storage pos = positions[msg.sender];

        uint256 collateralValueInETH;
        if (price > 0) {
            collateralValueInETH = (pos.tokenCollateral * 1e18) / price;
        }

        uint256 maxBorrow = (collateralValueInETH * RATIO_PRECISION) / COLLATERAL_RATIO;
        
        require(pos.ethDebt + amount <= maxBorrow, "Insufficient collateral");
        require(address(this).balance >= amount, "Insufficient pool liquidity");

        pos.ethDebt += amount;
        
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "ETH transfer failed");
        
        emit ETHBorrowed(msg.sender, amount);
    }

    function liquidate(address borrower) external {
        Position storage pos = positions[borrower];
        uint256 price = getOraclePrice();

        bool isUndercollateralized = false;

        if (pos.tokenDebt > 0) {
            uint256 requiredETH = (pos.tokenDebt * 1e18 * COLLATERAL_RATIO) / 
                                  (price * RATIO_PRECISION);
            if (pos.ethCollateral < requiredETH) {
                isUndercollateralized = true;
            }
        }

        if (pos.ethDebt > 0) {
            uint256 requiredTokens = (pos.ethDebt * price * COLLATERAL_RATIO) / 
                                     (1e18 * RATIO_PRECISION);
            if (pos.tokenCollateral < requiredTokens) {
                isUndercollateralized = true;
            }
        }

        require(isUndercollateralized, "Position is healthy");

        uint256 seizedETH = pos.ethCollateral;
        uint256 seizedTokens = pos.tokenCollateral;

        pos.ethCollateral = 0;
        pos.tokenDebt = 0;
        pos.tokenCollateral = 0;
        pos.ethDebt = 0;

        if (seizedETH > 0) {
            (bool success, ) = payable(msg.sender).call{value: seizedETH}("");
            require(success, "ETH transfer failed");
        }
        if (seizedTokens > 0) {
            token.transfer(msg.sender, seizedTokens);
        }

        emit PositionLiquidated(borrower, msg.sender);
    }

    function flashloan(uint256 amount, bytes calldata data) external {
        require(!_flashloanActive, "Flashloan already active");
        require(address(this).balance >= amount, "Insufficient liquidity");

        _flashloanActive = true;
        uint256 balanceBefore = address(this).balance;

        (bool success, ) = payable(msg.sender).call{value: amount}(data);
        require(success, "Flashloan callback failed");

        uint256 fee = (amount * FLASHLOAN_FEE) / FEE_PRECISION;
        require(
            address(this).balance >= balanceBefore + fee,
            "Flashloan not repaid"
        );

        _flashloanActive = false;
        emit FlashloanExecuted(msg.sender, amount);
    }

    function getPosition(address user) external view returns (
        uint256 ethCollateral,
        uint256 tokenDebt,
        uint256 tokenCollateral,
        uint256 ethDebt
    ) {
        Position memory pos = positions[user];
        return (pos.ethCollateral, pos.tokenDebt, pos.tokenCollateral, pos.ethDebt);
    }

    function poolETHBalance() external view returns (uint256) {
        return address(this).balance;
    }

    receive() external payable {}
}

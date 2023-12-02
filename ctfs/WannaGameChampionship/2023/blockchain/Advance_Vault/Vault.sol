// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./WannaETH.sol";
import "./PhantomToken.sol";

contract Vault {
    WannaETH public immutable weth;
    PhantomToken public immutable pmt;

    uint256 public totalDeposited;

    mapping(address => uint256) public deposited;

    modifier allowedAsset(address asset) {
        require(asset == address(weth) || asset == address(pmt), "Vault: INVALID_ASSET");
        _;
    }

    constructor(address payable _weth, address payable _pmt) {
        weth = WannaETH(_weth);
        pmt = PhantomToken(_pmt);
    }

    function deposit(address asset, uint256 amount) external allowedAsset(asset) {
        require(amount > 0, "Vault: ZERO");
        require(IERC20(asset).balanceOf(msg.sender) >= amount, "Vault: INSUFFICIENT_WETH");

        deposited[msg.sender] += amount;
        totalDeposited += amount;

        bool success = IERC20(asset).transferFrom(msg.sender, address(this), amount);
        require(success, "Vault: TRANSFER_FAILED");
    }

    function depositWithPermit(
        address asset,
        address from,
        uint256 amount,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external allowedAsset(asset) {
        require(amount > 0, "Vault: ZERO");
        require(IERC20(asset).balanceOf(from) >= amount, "Vault: INSUFFICIENT_WETH");
        deposited[msg.sender] += amount;
        totalDeposited += amount;
        PhantomToken(asset).permit(from, address(this), amount, deadline, v, r, s);
        bool success = PhantomToken(asset).transferFrom(from, address(this), amount);
        require(success, "Vault: TRANSFER_FAILED");
    }

    function withdraw(address asset, uint256 amount) external allowedAsset(asset) {
        require(amount > 0, "Vault: ZERO");
        require(deposited[msg.sender] >= amount, "Vault: INSUFFICIENT_DEPOSIT");

        deposited[msg.sender] -= amount;
        totalDeposited -= amount;

        bool success = IERC20(asset).transfer(msg.sender, amount);
        require(success, "Vault: TRANSFER_FAILED");
    }

    function claimFaucet() public {
        weth.transfer(msg.sender, 1);
        pmt.transfer(msg.sender, 1);
    }
}

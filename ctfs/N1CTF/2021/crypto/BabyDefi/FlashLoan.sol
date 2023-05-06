pragma solidity ^0.6.12;
import "./interface/IERC20.sol";
import "./library/SafeERC20.sol";

contract ReentrancyGuard {
    uint private _guardValue;
    modifier nonReentrant()
    {
        require(_guardValue == 0, "REENTRANCY");
        _guardValue = 1;
        _;
        _guardValue = 0;
    }
}

interface IflashLoanCallee{
    function flashLoanCall(
        address sender,
        IERC20 token,
        uint256 amountOut,
        bytes calldata data
    ) external;
}

contract FlashLoan is ReentrancyGuard{
    using SafeERC20 for IERC20;
    address tokenSupply; 
    constructor(address _tokenSupply) public {
        tokenSupply = _tokenSupply;
    }
    function flashloan(uint amountOut,bytes calldata data) public nonReentrant{
        uint balanceBefore = IERC20(tokenSupply).balanceOf(address(this));
        require(balanceBefore >= amountOut,"Not enough.");
        IERC20(tokenSupply).safeTransfer(msg.sender,amountOut);
        if (data.length > 0)
            IflashLoanCallee(msg.sender).flashLoanCall(address(this),IERC20(tokenSupply),amountOut,data);
        uint balanceAfter = IERC20(tokenSupply).balanceOf(address(this));
        require(balanceAfter >= balanceBefore,"FlashLoan Failed.");
    }
}

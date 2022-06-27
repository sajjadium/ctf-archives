pragma solidity ^0.8.0;

import "./token/ERC20/extensions/ERC20Votes.sol";
import "./interfaces/IERC3156FlashBorrower.sol";
import "./interfaces/IERC3156FlashLender.sol";

bytes32 constant _RETURN_VALUE = keccak256("ERC3156FlashBorrower.onFlashLoan");

contract AAA is ERC20Votes{
    constructor() ERC20("AToken", "AAA") ERC20Permit("AToken") {
        _mint(msg.sender, 100000000 * 10 ** decimals());
    }

    function maxFlashLoan(address token) public view returns (uint256) {
        return token == address(this) ? type(uint256).max - ERC20.totalSupply() : 0;
    }

    function flashFee(address token, uint256 amount) public view returns (uint256) {
        require(token == address(this));
        uint fee=amount/100;

        if(fee<10){
            return 10;
        }
        return fee;
    }

    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) public returns (bool) {
        require(amount <= maxFlashLoan(token));
        uint256 fee = flashFee(token, amount);
        _mint(address(receiver), amount);
        require(
            receiver.onFlashLoan(msg.sender, token, amount, fee, data) == _RETURN_VALUE
        );
        _spendAllowance(address(receiver), address(this), amount + fee);
        _burn(address(receiver), amount + fee);
        return true;
    }
}


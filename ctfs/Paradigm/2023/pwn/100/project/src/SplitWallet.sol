import "@clones-with-immutable-args/src/Clone.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SplitWallet is Clone {
    function deposit() external payable {}

    function pullToken(IERC20 token, uint256 amount) external {
        require(msg.sender == _getArgAddress(0));

        if (address(token) == address(0x00)) {
            payable(msg.sender).transfer(amount);
        } else {
            token.transfer(msg.sender, amount);
        }
    }

    function balanceOf(IERC20 token) external view returns (uint256) {
        if (address(token) == address(0x00)) {
            return address(this).balance;
        }

        return token.balanceOf(address(this));
    }
}

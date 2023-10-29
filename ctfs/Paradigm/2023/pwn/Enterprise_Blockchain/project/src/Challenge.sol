import "../lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";

contract Challenge {
    address public immutable BRIDGE;
    address public immutable FLAG_TOKEN;

    constructor(address bridge, address flagToken) {
        BRIDGE = bridge;
        FLAG_TOKEN = flagToken;
    }

    function isSolved() external view returns (bool) {
        return IERC20(FLAG_TOKEN).balanceOf(BRIDGE) < 90 ether;
    }
}

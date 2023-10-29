import "@openzeppelin/contracts/access/Ownable.sol";

import "./Account.sol";

contract SystemConfiguration is Ownable {
    address private accountImplementation;

    address private ethUsdPriceFeed;

    address private accountManager;

    address private stablecoin;

    uint256 private collateralRatio;

    mapping(address => bool) private _systemContracts;

    constructor() {
        collateralRatio = 15000;
    }

    function updateAccountImplementation(address newImplementation) external onlyOwner {
        accountImplementation = newImplementation;
    }

    function updateEthUsdPriceFeed(address newPriceFeed) external onlyOwner {
        ethUsdPriceFeed = newPriceFeed;
    }

    function updateStablecoin(address newStablecoin) external onlyOwner {
        stablecoin = newStablecoin;
    }

    function updateAccountManager(address newAccountManager) external onlyOwner {
        accountManager = newAccountManager;
    }

    function updateCollateralRatio(uint256 newRatio) external onlyOwner {
        collateralRatio = newRatio;
    }

    function updateSystemContract(address target, bool authorized) external onlyOwner {
        _systemContracts[target] = authorized;
    }

    function getAccountImplementation() external view returns (address) {
        return accountImplementation;
    }

    function getEthUsdPriceFeed() external view returns (address) {
        return ethUsdPriceFeed;
    }

    function getCollateralRatio() external view returns (uint256) {
        return collateralRatio;
    }

    function getStablecoin() external view returns (address) {
        return stablecoin;
    }

    function getAccountManager() external view returns (address) {
        return accountManager;
    }

    function isAuthorized(address who) external view returns (bool) {
        return _systemContracts[who];
    }
}

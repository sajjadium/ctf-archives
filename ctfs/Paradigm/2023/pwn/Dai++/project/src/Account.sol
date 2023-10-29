import "@clones-with-immutable-args/src/Clone.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/cryptography/SignatureChecker.sol";

import "./SystemConfiguration.sol";
import "./AccountManager.sol";

contract Account is Clone {
    event DebtIncreased(uint256 amount, string memo);
    event DebtDecreased(uint256 amount, string memo);

    uint256 private debt;

    function deposit() external payable {}

    function withdraw(uint256 amount) external {
        require(msg.sender == _getArgAddress(20), "ONLY_ACCOUNT_HOLDER");

        require(isHealthy(amount, 0), "NOT_HEALTHY");

        (bool ok,) = payable(msg.sender).call{value: amount}(hex"");
        require(ok, "TRANSFER_FAILED");
    }

    function increaseDebt(address operator, uint256 amount, string calldata memo) external {
        SystemConfiguration configuration = SystemConfiguration(_getArgAddress(0));
        require(configuration.isAuthorized(msg.sender), "NOT_AUTHORIZED");

        require(operator == _getArgAddress(20), "ONLY_ACCOUNT_HOLDER");

        require(isHealthy(0, amount), "NOT_HEALTHY");

        debt += amount;

        emit DebtIncreased(amount, memo);
    }

    function decreaseDebt(uint256 amount, string calldata memo) external {
        SystemConfiguration configuration = SystemConfiguration(_getArgAddress(0));
        require(configuration.isAuthorized(msg.sender), "NOT_AUTHORIZED");

        debt -= amount;

        emit DebtDecreased(amount, memo);
    }

    function isHealthy(uint256 collateralDecrease, uint256 debtIncrease) public view returns (bool) {
        SystemConfiguration configuration = SystemConfiguration(_getArgAddress(0));

        uint256 totalBalance = address(this).balance - collateralDecrease;
        uint256 totalDebt = debt + debtIncrease;

        (, int256 ethPriceInt,,,) = AggregatorV3Interface(configuration.getEthUsdPriceFeed()).latestRoundData();
        if (ethPriceInt <= 0) return false;

        uint256 ethPrice = uint256(ethPriceInt);

        return totalBalance * ethPrice / 1e8 >= totalDebt * configuration.getCollateralRatio() / 10000;
    }

    function recoverAccount(address newOwner, address[] memory newRecoveryAccounts, bytes[] memory signatures)
        external
        returns (Account)
    {
        require(isHealthy(0, 0), "UNHEALTHY_ACCOUNT");

        bytes32 signHash = keccak256(abi.encodePacked(block.chainid, _getArgAddress(20), newOwner, newRecoveryAccounts));

        uint256 numRecoveryAccounts = _getArgUint256(40);
        require(signatures.length == numRecoveryAccounts, "INCORRECT_LENGTH");

        for (uint256 i = 0; i < numRecoveryAccounts; i++) {
            require(
                SignatureChecker.isValidSignatureNow(_getArgAddress(72 + 32 * i), signHash, signatures[i]),
                "INVALID_SIGNATURE"
            );
        }

        SystemConfiguration configuration = SystemConfiguration(_getArgAddress(0));

        uint256 currentDebt = debt;
        debt = 0;

        return AccountManager(configuration.getAccountManager()).migrateAccount{value: address(this).balance}(
            newOwner, newRecoveryAccounts, currentDebt
        );
    }
}

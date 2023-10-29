import "@clones-with-immutable-args/src/ClonesWithImmutableArgs.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./Account.sol";
import "./Stablecoin.sol";

contract AccountManager {
    using ClonesWithImmutableArgs for address;

    SystemConfiguration private immutable SYSTEM_CONFIGURATION;

    mapping(Account => bool) public validAccounts;

    constructor(SystemConfiguration configuration) {
        SYSTEM_CONFIGURATION = configuration;
    }

    modifier onlyValidAccount(Account account) {
        require(validAccounts[account], "INVALID_ACCOUNT");
        _;
    }

    function openAccount(address owner, address[] calldata recoveryAddresses) external returns (Account) {
        return _openAccount(owner, recoveryAddresses);
    }

    function migrateAccount(address owner, address[] calldata recoveryAddresses, uint256 debt)
        external
        payable
        returns (Account)
    {
        Account account = _openAccount(owner, recoveryAddresses);
        account.deposit{value: msg.value}();

        account.increaseDebt(owner, debt, "account migration");
        return account;
    }

    function _openAccount(address owner, address[] calldata recoveryAddresses) private returns (Account) {
        Account account = Account(
            SYSTEM_CONFIGURATION.getAccountImplementation().clone(
                abi.encodePacked(SYSTEM_CONFIGURATION, owner, recoveryAddresses.length, recoveryAddresses)
            )
        );

        validAccounts[account] = true;

        return account;
    }

    function mintStablecoins(Account account, uint256 amount, string calldata memo)
        external
        onlyValidAccount(account)
    {
        account.increaseDebt(msg.sender, amount, memo);

        Stablecoin(SYSTEM_CONFIGURATION.getStablecoin()).mint(msg.sender, amount);
    }

    function burnStablecoins(Account account, uint256 amount, string calldata memo)
        external
        onlyValidAccount(account)
    {
        account.decreaseDebt(amount, memo);

        Stablecoin(SYSTEM_CONFIGURATION.getStablecoin()).burn(msg.sender, amount);
    }
}

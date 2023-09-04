pragma solidity ^0.8.19;

import "@openzeppelin/contracts/proxy/Proxy.sol";
import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Upgrade.sol";

// https://tenor.com/view/fadsfantasy-monkey-phone-mono-tel%C3%A9fono-george-monkey-gif-26110826
contract MonkeingAround {
    address[] public allowlisted;
    address public owner;

    error AddressAlreadyAllowlisted(address);
    error AddressNotAllowlisted(address);
    error NotOwner();
    error CallFailed();

    event AddressAddedToAllowList(address indexed);

    // Allowlist both the proxy and implementation, just to be safe
    constructor() {
        owner = msg.sender;
        MonkeMath imp = new MonkeMath();
        InitializableProxy proxy = new InitializableProxy(address(imp), "");
        addToAllowlist(address(proxy));
        addToAllowlist(address(imp));
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    function addToAllowlist(address _address) public onlyOwner {
        if (isInAllowlist(_address)) revert AddressAlreadyAllowlisted(_address);
        allowlisted.push(_address);
        emit AddressAddedToAllowList(_address);
    }

    function isInAllowlist(address _address) public view returns (bool) {
        for (uint256 i = 0; i < allowlisted.length; i++) {
            if (allowlisted[i] == _address) return true;
        }
        return false;
    }

    function allowlistCount() public view returns (uint256) {
        return allowlisted.length;
    }

    // Call to safe monkes only
    function doSomeMonkeMath(address _address, bytes calldata data) external returns (bytes memory) {
        if (!isInAllowlist(_address)) revert AddressNotAllowlisted(_address);
        (bool succ, bytes memory res) = _address.delegatecall(data);
        if (!succ) revert CallFailed();
        return res;
    }
}

// Monke ooo la la monke
// https://tenor.com/view/orangutan-driving-gif-24461244
contract MonkeMath {
    event Ooo_ooo_OOO_AAAA_AAAAAH();

    // https://tenor.com/view/krach-boursier-calculate-monkey-silly-gif-14808948
    function monkeAdd(uint256 a, uint256 b) external returns (uint256) {
        emit Ooo_ooo_OOO_AAAA_AAAAAH();
        return a + b;
    }

    // https://tenor.com/view/monkey-gif-19404599
    function monkeSubtract(uint256 a, uint256 b) external returns (uint256) {
        emit Ooo_ooo_OOO_AAAA_AAAAAH();
        return a - b;
    }
}

contract InitializableProxy is Proxy, ERC1967Upgrade {
    constructor(address _logic, bytes memory data) {
        init(_logic, data);
    }

    function init(address _logic, bytes memory data) public {
        if (_implementation() != address(0)) revert("Already initialized");
        _upgradeToAndCall(_logic, data, false);
    }

    function _implementation() internal view virtual override returns (address impl) {
        return ERC1967Upgrade._getImplementation();
    }
}

pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IBridge} from "./IBridge.sol";

contract FlagToken is ERC20 {
    constructor(address bridge, address user) ERC20("FLAG Token", "FTT") {
        _mint(bridge, 100 ether);
        _mint(user, 1 ether);
    }
}

contract BridgedERC20 is ERC20 {
    IBridge public immutable BRIDGE;
    address public immutable REMOTE_TOKEN;

    modifier onlyBridge() {
        require(msg.sender == address(BRIDGE), "B");
        _;
    }

    modifier onlyRemoteBridge() {
        require(msg.sender == address(BRIDGE), "RB1");
        require(
            BRIDGE.relayedMessageSenderChainId() != 0
                && BRIDGE.remoteBridgeChainId(BRIDGE.relayedMessageSenderAddress()) == BRIDGE.relayedMessageSenderChainId(),
            "RB2"
        );
        _;
    }

    constructor(address _remoteToken, string memory _name, string memory _symbol) ERC20(_name, _symbol) {
        BRIDGE = IBridge(msg.sender);
        REMOTE_TOKEN = _remoteToken;
    }

    function mint(address _to, uint256 _amount) external onlyRemoteBridge {
        _mint(_to, _amount);
    }

    function burn(address _from, uint256 _amount) external onlyBridge {
        _burn(_from, _amount);
    }
}

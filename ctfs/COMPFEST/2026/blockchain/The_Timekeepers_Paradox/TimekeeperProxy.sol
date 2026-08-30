// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimekeeperProxy {
    address public admin;

    address public implementation;

    address public pendingAdmin;

    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

    mapping(address => bool) public validImplementations;

    event Upgraded(address indexed newImplementation);
    event AdminChanged(address indexed newAdmin);
    event PendingAdminSet(address indexed pendingAdmin);

    constructor(address _implementation) {
        admin = msg.sender;
        implementation = _implementation;
        validImplementations[_implementation] = true;

        assembly {
            sstore(
                0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc,
                _implementation
            )
        }
    }

    function setPendingAdmin(address _pendingAdmin) external {
        require(msg.sender == address(this), "Only self");
        pendingAdmin = _pendingAdmin;
        emit PendingAdminSet(_pendingAdmin);
    }

    function acceptAdmin() external {
        require(msg.sender == pendingAdmin, "Not pending admin");
        admin = pendingAdmin;
        pendingAdmin = address(0);
        emit AdminChanged(admin);
    }

    function upgradeTo(address newImplementation) external {
        require(msg.sender == admin, "Only admin");
        require(validImplementations[newImplementation], "Invalid implementation");
        
        implementation = newImplementation;

        assembly {
            sstore(
                0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc,
                newImplementation
            )
        }

        emit Upgraded(newImplementation);
    }

    function registerImplementation(address impl) external {
        require(msg.sender == admin, "Only admin");
        validImplementations[impl] = true;
    }

    function multicall(bytes[] calldata data) external returns (bytes[] memory results) {
        results = new bytes[](data.length);
        for (uint256 i = 0; i < data.length; i++) {
            (bool success, bytes memory result) = address(this).call(data[i]);
            require(success, "Multicall: call failed");
            results[i] = result;
        }
    }

    fallback() external payable {
        address impl = implementation;
        require(impl != address(0), "No implementation");

        assembly {
            calldatacopy(0, 0, calldatasize())

            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)

            returndatacopy(0, 0, returndatasize())

            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }

    receive() external payable {}
}

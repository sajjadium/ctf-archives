// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IERC1155ReceiverUpgradeable } from "../../token/ERC1155/IERC1155ReceiverUpgradeable.sol";
import { ERC165Upgradeable } from "../../utils/introspection/ERC165Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC1155ReceiverMockUpgradeable is Initializable, ERC165Upgradeable, IERC1155ReceiverUpgradeable {
    enum RevertType {
        None,
        RevertWithoutMessage,
        RevertWithMessage,
        RevertWithCustomError,
        Panic
    }

    bytes4 private _recRetval;
    bytes4 private _batRetval;
    RevertType private _error;

    event Received(address operator, address from, uint256 id, uint256 value, bytes data, uint256 gas);
    event BatchReceived(address operator, address from, uint256[] ids, uint256[] values, bytes data, uint256 gas);
    error CustomError(bytes4);

    function __ERC1155ReceiverMock_init(bytes4 recRetval, bytes4 batRetval, RevertType error) internal onlyInitializing {
        __ERC1155ReceiverMock_init_unchained(recRetval, batRetval, error);
    }

    function __ERC1155ReceiverMock_init_unchained(bytes4 recRetval, bytes4 batRetval, RevertType error) internal onlyInitializing {
        _recRetval = recRetval;
        _batRetval = batRetval;
        _error = error;
    }

    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4) {
        if (_error == RevertType.RevertWithoutMessage) {
            revert();
        } else if (_error == RevertType.RevertWithMessage) {
            revert("ERC1155ReceiverMock: reverting on receive");
        } else if (_error == RevertType.RevertWithCustomError) {
            revert CustomError(_recRetval);
        } else if (_error == RevertType.Panic) {
            uint256 a = uint256(0) / uint256(0);
            a;
        }

        emit Received(operator, from, id, value, data, gasleft());
        return _recRetval;
    }

    function onERC1155BatchReceived(
        address operator,
        address from,
        uint256[] calldata ids,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4) {
        if (_error == RevertType.RevertWithoutMessage) {
            revert();
        } else if (_error == RevertType.RevertWithMessage) {
            revert("ERC1155ReceiverMock: reverting on batch receive");
        } else if (_error == RevertType.RevertWithCustomError) {
            revert CustomError(_recRetval);
        } else if (_error == RevertType.Panic) {
            uint256 a = uint256(0) / uint256(0);
            a;
        }

        emit BatchReceived(operator, from, ids, values, data, gasleft());
        return _batRetval;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

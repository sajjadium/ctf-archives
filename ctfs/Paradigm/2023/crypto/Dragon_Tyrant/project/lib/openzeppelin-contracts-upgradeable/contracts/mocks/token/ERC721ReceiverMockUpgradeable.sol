// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { IERC721ReceiverUpgradeable } from "../../token/ERC721/IERC721ReceiverUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC721ReceiverMockUpgradeable is Initializable, IERC721ReceiverUpgradeable {
    enum RevertType {
        None,
        RevertWithoutMessage,
        RevertWithMessage,
        RevertWithCustomError,
        Panic
    }

    bytes4 private _retval;
    RevertType private _error;

    event Received(address operator, address from, uint256 tokenId, bytes data, uint256 gas);
    error CustomError(bytes4);

    function __ERC721ReceiverMock_init(bytes4 retval, RevertType error) internal onlyInitializing {
        __ERC721ReceiverMock_init_unchained(retval, error);
    }

    function __ERC721ReceiverMock_init_unchained(bytes4 retval, RevertType error) internal onlyInitializing {
        _retval = retval;
        _error = error;
    }

    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes memory data
    ) public returns (bytes4) {
        if (_error == RevertType.RevertWithoutMessage) {
            revert();
        } else if (_error == RevertType.RevertWithMessage) {
            revert("ERC721ReceiverMock: reverting");
        } else if (_error == RevertType.RevertWithCustomError) {
            revert CustomError(_retval);
        } else if (_error == RevertType.Panic) {
            uint256 a = uint256(0) / uint256(0);
            a;
        }

        emit Received(operator, from, tokenId, data, gasleft());
        return _retval;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

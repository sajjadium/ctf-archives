// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC721Upgradeable } from "../../token/ERC721/ERC721Upgradeable.sol";
import { ERC721ConsecutiveUpgradeable } from "../../token/ERC721/extensions/ERC721ConsecutiveUpgradeable.sol";
import { ERC721PausableUpgradeable } from "../../token/ERC721/extensions/ERC721PausableUpgradeable.sol";
import { ERC721VotesUpgradeable } from "../../token/ERC721/extensions/ERC721VotesUpgradeable.sol";
import { EIP712Upgradeable } from "../../utils/cryptography/EIP712Upgradeable.sol";
import "../../proxy/utils/Initializable.sol";

/**
 * @title ERC721ConsecutiveMock
 */
contract ERC721ConsecutiveMockUpgradeable is Initializable, ERC721ConsecutiveUpgradeable, ERC721PausableUpgradeable, ERC721VotesUpgradeable {
    uint96 private _offset;

    function __ERC721ConsecutiveMock_init(
        string memory name,
        string memory symbol,
        uint96 offset,
        address[] memory delegates,
        address[] memory receivers,
        uint96[] memory amounts
    ) internal onlyInitializing {
        __ERC721_init_unchained(name, symbol);
        __Pausable_init_unchained();
        __EIP712_init_unchained(name, "1");
        __ERC721ConsecutiveMock_init_unchained(name, symbol, offset, delegates, receivers, amounts);
    }

    function __ERC721ConsecutiveMock_init_unchained(
        string memory,
        string memory,
        uint96 offset,
        address[] memory delegates,
        address[] memory receivers,
        uint96[] memory amounts
    ) internal onlyInitializing {
        _offset = offset;

        for (uint256 i = 0; i < delegates.length; ++i) {
            _delegate(delegates[i], delegates[i]);
        }

        for (uint256 i = 0; i < receivers.length; ++i) {
            _mintConsecutive(receivers[i], amounts[i]);
        }
    }

    function _firstConsecutiveId() internal view virtual override returns (uint96) {
        return _offset;
    }

    function _ownerOf(uint256 tokenId) internal view virtual override(ERC721Upgradeable, ERC721ConsecutiveUpgradeable) returns (address) {
        return super._ownerOf(tokenId);
    }

    function _mint(address to, uint256 tokenId) internal virtual override(ERC721Upgradeable, ERC721ConsecutiveUpgradeable) {
        super._mint(to, tokenId);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 firstTokenId,
        uint256 batchSize
    ) internal virtual override(ERC721Upgradeable, ERC721PausableUpgradeable) {
        super._beforeTokenTransfer(from, to, firstTokenId, batchSize);
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 firstTokenId,
        uint256 batchSize
    ) internal virtual override(ERC721Upgradeable, ERC721VotesUpgradeable, ERC721ConsecutiveUpgradeable) {
        super._afterTokenTransfer(from, to, firstTokenId, batchSize);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

contract ERC721ConsecutiveNoConstructorMintMockUpgradeable is Initializable, ERC721ConsecutiveUpgradeable {
    function __ERC721ConsecutiveNoConstructorMintMock_init(string memory name, string memory symbol) internal onlyInitializing {
        __ERC721_init_unchained(name, symbol);
        __ERC721ConsecutiveNoConstructorMintMock_init_unchained(name, symbol);
    }

    function __ERC721ConsecutiveNoConstructorMintMock_init_unchained(string memory, string memory) internal onlyInitializing {
        _mint(msg.sender, 0);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}

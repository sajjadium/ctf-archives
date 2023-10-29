// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC721Upgradeable } from "../../token/ERC721/ERC721Upgradeable.sol";
import { ERC721ConsecutiveUpgradeable } from "../../token/ERC721/extensions/ERC721ConsecutiveUpgradeable.sol";
import { ERC721EnumerableUpgradeable } from "../../token/ERC721/extensions/ERC721EnumerableUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

contract ERC721ConsecutiveEnumerableMockUpgradeable is Initializable, ERC721ConsecutiveUpgradeable, ERC721EnumerableUpgradeable {
    function __ERC721ConsecutiveEnumerableMock_init(
        string memory name,
        string memory symbol,
        address[] memory receivers,
        uint96[] memory amounts
    ) internal onlyInitializing {
        __ERC721_init_unchained(name, symbol);
        __ERC721ConsecutiveEnumerableMock_init_unchained(name, symbol, receivers, amounts);
    }

    function __ERC721ConsecutiveEnumerableMock_init_unchained(
        string memory,
        string memory,
        address[] memory receivers,
        uint96[] memory amounts
    ) internal onlyInitializing {
        for (uint256 i = 0; i < receivers.length; ++i) {
            _mintConsecutive(receivers[i], amounts[i]);
        }
    }

    function supportsInterface(
        bytes4 interfaceId
    ) public view virtual override(ERC721Upgradeable, ERC721EnumerableUpgradeable) returns (bool) {
        return super.supportsInterface(interfaceId);
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
    ) internal virtual override(ERC721Upgradeable, ERC721EnumerableUpgradeable) {
        super._beforeTokenTransfer(from, to, firstTokenId, batchSize);
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 firstTokenId,
        uint256 batchSize
    ) internal virtual override(ERC721Upgradeable, ERC721ConsecutiveUpgradeable) {
        super._afterTokenTransfer(from, to, firstTokenId, batchSize);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}

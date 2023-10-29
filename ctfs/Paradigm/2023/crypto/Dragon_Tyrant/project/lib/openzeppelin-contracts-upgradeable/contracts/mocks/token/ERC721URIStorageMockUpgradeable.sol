// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ERC721URIStorageUpgradeable } from "../../token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "../../proxy/utils/Initializable.sol";

abstract contract ERC721URIStorageMockUpgradeable is Initializable, ERC721URIStorageUpgradeable {
    function __ERC721URIStorageMock_init() internal onlyInitializing {
    }

    function __ERC721URIStorageMock_init_unchained() internal onlyInitializing {
    }
    string private _baseTokenURI;

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    function setBaseURI(string calldata newBaseTokenURI) public {
        _baseTokenURI = newBaseTokenURI;
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[49] private __gap;
}

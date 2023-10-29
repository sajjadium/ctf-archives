// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.9.0) (interfaces/IERC4906.sol)

pragma solidity ^0.8.19;

import { IERC165Upgradeable } from "./IERC165Upgradeable.sol";
import { IERC721Upgradeable } from "./IERC721Upgradeable.sol";

/// @title EIP-721 Metadata Update Extension
interface IERC4906Upgradeable is IERC165Upgradeable, IERC721Upgradeable {
    /// @dev This event emits when the metadata of a token is changed.
    /// So that the third-party platforms such as NFT market could
    /// timely update the images and related attributes of the NFT.
    event MetadataUpdate(uint256 _tokenId);

    /// @dev This event emits when the metadata of a range of tokens is changed.
    /// So that the third-party platforms such as NFT market could
    /// timely update the images and related attributes of the NFTs.
    event BatchMetadataUpdate(uint256 _fromTokenId, uint256 _toTokenId);
}

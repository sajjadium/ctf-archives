// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import { ECDSAUpgradeable } from "../utils/cryptography/ECDSAUpgradeable.sol";
import { EIP712Upgradeable } from "../utils/cryptography/EIP712Upgradeable.sol";
import "../proxy/utils/Initializable.sol";

abstract contract EIP712VerifierUpgradeable is Initializable, EIP712Upgradeable {
    function __EIP712Verifier_init() internal onlyInitializing {
    }

    function __EIP712Verifier_init_unchained() internal onlyInitializing {
    }
    function verify(bytes memory signature, address signer, address mailTo, string memory mailContents) external view {
        bytes32 digest = _hashTypedDataV4(
            keccak256(abi.encode(keccak256("Mail(address to,string contents)"), mailTo, keccak256(bytes(mailContents))))
        );
        address recoveredSigner = ECDSAUpgradeable.recover(digest, signature);
        require(recoveredSigner == signer);
    }

    /**
     * @dev This empty reserved space is put in place to allow future versions to add new
     * variables without shifting down storage in the inheritance chain.
     * See https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps
     */
    uint256[50] private __gap;
}

// SPDX-License-Identifier: MIT
pragma solidity >0.5.0 <0.9.0;

import {ICrossDomainMessenger} from "./ICrossDomainMessenger.sol";

contract CrossDomainEnabled {
    // Messenger contract used to send and recieve messages from the other domain.
    address public messenger;

    /**
     * @param _messenger Address of the CrossDomainMessenger on the current layer.
     */
    constructor(address _messenger) {
        messenger = _messenger;
    }

    /**
     * Enforces that the modified function is only callable by a specific cross-domain account.
     * @param _sourceDomainAccount The only account on the originating domain which is
     *  authenticated to call this function.
     */
    modifier onlyFromCrossDomainAccount(address _sourceDomainAccount) {
        require(msg.sender == address(getCrossDomainMessenger()), "messenger contract unauthenticated");

        require(
            getCrossDomainMessenger().xDomainMessageSender() == _sourceDomainAccount,
            "wrong sender of cross-domain message"
        );

        _;
    }

    /**
     * Gets the messenger, usually from storage. This function is exposed in case a child contract
     * needs to override.
     * @return The address of the cross-domain messenger contract which should be used.
     */
    function getCrossDomainMessenger() internal virtual returns (ICrossDomainMessenger) {
        return ICrossDomainMessenger(messenger);
    }

    /**
     * Sends a message to an account on another domain
     * @param _crossDomainTarget The intended recipient on the destination domain
     * @param _message The data to send to the target (usually calldata to a function with
     *  `onlyFromCrossDomainAccount()`)
     */
    function sendCrossDomainMessage(address _crossDomainTarget, bytes memory _message) internal {
        getCrossDomainMessenger().sendMessage(_crossDomainTarget, _message);
    }
}

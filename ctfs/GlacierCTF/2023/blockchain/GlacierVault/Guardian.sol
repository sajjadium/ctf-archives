// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract Guardian
{
    bool public asleep;
    address public implementation_addr;
    uint256 people_mauled;
    address public owner;

    event putToSleepCall(address, address);

    constructor(address _implementation_addr)
    {
        asleep = false;
        implementation_addr = _implementation_addr;
        owner = msg.sender;
        people_mauled = 0;
    }

    function putToSleep() external
    {
        emit putToSleepCall(msg.sender, owner);
        require(msg.sender == owner, "You can't do that. The yeti mauls you.");
        asleep = true;
    }

    function punch() external payable
    {
        if (msg.value > 10_000_000 ether)
        {
            asleep = true;
        }
        else
        {
            people_mauled += 1;
        }
    }

    function _delegate(address implementation) internal {
        assembly {
            // Copy msg.data. We take full control of memory in this inline assembly
            // block because it will not return to Solidity code. We overwrite the
            // Solidity scratch pad at memory position 0.
            calldatacopy(0, 0, calldatasize())

            // Call the implementation.
            // out and outsize are 0 because we don't know the size yet.
            let result := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)

            // Copy the returned data.
            returndatacopy(0, 0, returndatasize())

            switch result
            // delegatecall returns 0 on error.
            case 0 {
                revert(0, returndatasize())
            }
            default {
                return(0, returndatasize())
            }
        }
    }

    /**
     * @dev This is a virtual function that should be overridden so it returns the address to which the fallback function
     * and {_fallback} should delegate.
     */
    function _implementation() internal view returns (address)
    {
        return implementation_addr;
    }

    /**
     * @dev Delegates the current call to the address returned by `_implementation()`.
     *
     * This function does not return to its internal call site, it will return directly to the external caller.
     */
    function _fallback() internal {
        _beforeFallback();
        _delegate(_implementation());
    }

    /**
     * @dev Fallback function that delegates calls to the address returned by `_implementation()`. Will run if no other
     * function in the contract matches the call data.
     */
    fallback() external payable {
        _fallback();
    }

    /**
     * @dev Hook that is called before falling back to the implementation. Can happen as part of a manual `_fallback`
     * call, or as part of the Solidity `fallback` or `receive` functions.
     *
     * If overridden should call `super._beforeFallback()`.
     */
    function _beforeFallback() internal {}
}
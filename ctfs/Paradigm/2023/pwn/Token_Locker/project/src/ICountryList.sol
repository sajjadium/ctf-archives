// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.19;

/**
 * @dev Interface of the CountryList contract
 */
interface ICountryList {
    function countryIsValid(uint16 _countryCode) external view returns (bool);
}

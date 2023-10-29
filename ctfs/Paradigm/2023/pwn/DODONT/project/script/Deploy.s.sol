// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Script.sol";
import "forge-ctf/CTFDeployment.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "src/Challenge.sol";

interface CloneFactoryLike {
    function clone(address) external returns (address);
}

interface DVMLike {
    function init(
        address maintainer,
        address baseTokenAddress,
        address quoteTokenAddress,
        uint256 lpFeeRate,
        address mtFeeRateModel,
        uint256 i,
        uint256 k,
        bool isOpenTWAP
    ) external;

    function buyShares(address) external;
}

contract QuoteToken is ERC20 {
    constructor() ERC20("Quote Token", "QT") {
        _mint(msg.sender, 1_000_000 ether);
    }
}

contract Deploy is CTFDeployment {
    CloneFactoryLike private immutable CLONE_FACTORY = CloneFactoryLike(0x5E5a7b76462E4BdF83Aa98795644281BdbA80B88);
    address private immutable DVM_TEMPLATE = 0x2BBD66fC4898242BDBD2583BBe1d76E8b8f71445;

    IERC20 private immutable WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

    function deploy(address system, address) internal override returns (address challenge) {
        vm.startBroadcast(system);

        payable(address(WETH)).call{value: 100 ether}(hex"");

        QuoteToken quoteToken = new QuoteToken();

        DVMLike dvm = DVMLike(CLONE_FACTORY.clone(DVM_TEMPLATE));
        dvm.init(
            address(system),
            address(WETH),
            address(quoteToken),
            3000000000000000,
            address(0x5e84190a270333aCe5B9202a3F4ceBf11b81bB01),
            1,
            1000000000000000000,
            false
        );

        WETH.transfer(address(dvm), WETH.balanceOf(address(system)));
        quoteToken.transfer(address(dvm), quoteToken.balanceOf(address(system)) / 2);
        dvm.buyShares(address(system));

        challenge = address(new Challenge(address(dvm)));

        vm.stopBroadcast();
    }
}

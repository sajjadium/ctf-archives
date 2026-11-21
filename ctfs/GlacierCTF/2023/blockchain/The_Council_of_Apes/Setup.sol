// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IcyExchange.sol";


contract Setup {
    IcyExchange public immutable TARGET; // Contract the player will hack
    IERC20 public monkeyToken;
    IERC20 public djungleCoin;
    bool public already_claimed;

    constructor() payable {
        // Deploy the target contract
        TARGET = new IcyExchange{value: 5 ether}();

        //Become an ape
        bytes32 holyWords = keccak256("I hereby swear to ape into every shitcoin I see, to never sell, to never surrender, to never give up, to never stop buying, to never stop hodling, to never stop aping, to never stop believing, to never stop dreaming, to never stop hoping, to never stop loving, to never stop living, to never stop breathing");
        TARGET.council().becomeAnApe(holyWords);

        // We generate 2 new tokens and deploy them at the exchange
        monkeyToken = new TotallyNotCopiedToken(address(this), "MonkeyToken", "MONK");
        djungleCoin = new TotallyNotCopiedToken(address(this), "DjungleCoin", "DJUNGLE");

        //Approve the exchange for both
        monkeyToken.approve(address(TARGET), 100_000);
        djungleCoin.approve(address(TARGET), 100_000);

        //Deploy both pools
        TARGET.createPool{value: 1 ether}(address(monkeyToken));
        TARGET.createPool{value: 1 ether}(address(djungleCoin));
    }

    //You can get 100 of each for free
    function claimFreeTokens() external
    {
        require(!already_claimed);
        monkeyToken.transfer(msg.sender, 100);
        djungleCoin.transfer(msg.sender, 100);
        already_claimed = true;
    }

    // Our challenge in the CTF framework will call this function to
    // check whether the player has solved the challenge or not.
    function isSolved() public view returns (bool) {
        return TARGET.council().isDissolved();
    }
}
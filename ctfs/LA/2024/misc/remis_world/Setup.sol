// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

import "./Remis.sol";

contract Setup {
    Remis public immutable remis;
    ShadyEchnida public immutable shady;

    constructor() {
        remis = new Remis();
        shady = new ShadyEchnida(remis);
    }

    function isSolved() external view returns (bool) {
        return shady.checkWallet() >= 100;
    }
}

contract ShadyEchnida {
    Remis private remis;

    constructor(Remis addr) {
        remis = addr;
        remis.openAccount();
    }

    function doFlavortext() public {
        remis.postBulletin("Look, kid. There's something... sus about all the vibrancy here at Remi's.");
        remis.postBulletin("I have a feeling there's something more to this shop than just tasteless burgers.");
        remis.postBulletin("...");
        remis.postBulletin("...");
        remis.postBulletin("I see I've perked your interest.");
        remis.postBulletin("Hmm...");
        remis.postBulletin("This type of Business isn't for a tiny hedgehog like you.");
        remis.postBulletin("You'll have to prove yourself, pull your own weight.");
        remis.postBulletin("...I can see that won't stop you.");
        remis.postBulletin("Fine. Want in? Give me $100, and I'll let you join the team.");
    }

    function checkWallet() public view returns (uint) {
        return remis.checkWallet();
    }
}

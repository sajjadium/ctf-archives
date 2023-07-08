pragma solidity ^0.8.0;

import "./crewToken.sol";
import "./respectToken.sol";
import "./candyToken.sol";
import "./fancyStore.sol";
import "./localGang.sol";

contract Setup {

    crewToken public immutable CREW;
    respectToken public immutable RESPECT;
    candyToken public immutable CANDY;
    fancyStore public immutable STORE;
    localGang public immutable GANG;

    constructor() payable {

        CREW = new crewToken();
        RESPECT = new respectToken();
        CANDY = new candyToken();   
        STORE = new fancyStore(address(CANDY), address(RESPECT), address(CREW));
        GANG = new localGang(address(CANDY), address(RESPECT));

        RESPECT.transferOwnership(address(GANG));
        CANDY.transferOwnership(address(STORE));


    }

    function isSolved() public view returns (bool) {
        return STORE.respectCount(CREW.receiver())>=50 ;
    }
}

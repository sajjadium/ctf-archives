import "src/ISimpleBank.sol";

contract Challenge {
    ISimpleBank public immutable BANK;

    constructor(ISimpleBank bank) {
        BANK = bank;
    }

    function isSolved() external view returns (bool) {
        return address(BANK).balance == 0;
    }
}

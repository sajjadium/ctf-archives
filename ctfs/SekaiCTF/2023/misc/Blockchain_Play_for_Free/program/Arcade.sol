
@program_id("ArciEpQvGwZk5yegHEiy27afRZaDLKU8B3kj5MWc38rq")
contract Arcade {
    int32 public tokens;
    uint32 public playCount;
    uint64 private forgotten;
    uint64[] private stuckInGap;
    uint64[1] private atBottom;
    address private somewhere;
    string private lookForIt;

    @payer(payer)
    @space(160)
    constructor(uint64[3] memory locations, address _addr, string memory _loc) {
        // drop some tokens :>
        forgotten = locations[0];
        stuckInGap.push(locations[1]);
        atBottom[0] = locations[2];
        somewhere = _addr;
        lookForIt = _loc;
    }

    // find_string_uint64
    function find(string calldata machine, uint64 location) external {
        require(tx.accounts[0].owner == type(Arcade).program_id, "Invalid");
        if (machine == "Token Dispenser") {
            if (location == forgotten && (tokens & 1 == 0)) {
                tokens ^= 1;
                print("Picked it up owo");
                return;
            }
        } else if (machine == "Token Counter") {
            if (location == stuckInGap[0] && (tokens & 2 == 0)) {
                tokens ^= 2;
                print("Saved it >w<");
                return;
            }
        } else if (machine == "Arcade Machine") {
            if (location == atBottom[0] && (tokens & 4 == 0)) {
                tokens ^= 4;
                print("Got it :3");
                return;
            }
        }
        print("Nothing here :(");
    }

    // find_bytes32
    function find(address location) external {
        require(tx.accounts[0].owner == type(Arcade).program_id, "Invalid");
        if (location == somewhere && (tokens & 8 == 0)) {
            tokens ^= 8;
            print("Found it :D");
            return;
        }
        print("Nothing here :(");
    }

    // find_string
    function find(string calldata location) external {
        require(tx.accounts[0].owner == type(Arcade).program_id, "Invalid");
        if(location == lookForIt && (tokens & 16 == 0)) {
            tokens ^= 16;
            print("!!!");
            return;
        }
        print("Nothing here :(");
    }

    function play() external {
        require(tx.accounts[0].owner == type(Arcade).program_id, "Invalid");
        if (tokens == 0x1f) {
            playCount++;
            print("Played 1pc for FREE! XD");
            tokens = -1; // Σ(0v0)
            return;
        } else if (tokens != -1) {
            uint32 cnt = 0;
            for (uint8 i = 0; i < 5; ) {
                if (tokens & (1 << i) > 0) {
                    cnt++;
                }
                unchecked {
                    ++i;
                }
            }
            print("{} / 5 ...".format(cnt));
            return;
        }
    }
}

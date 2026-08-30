// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimekeeperOracle {
    address public admin;

    address public reporter;

    uint256 public latestPrice;

    bytes32 private constant PRICE_SLOT = keccak256("timekeeper.oracle.price");

    struct Observation {
        uint256 timestamp;
        uint256 cumulativePrice;
    }

    Observation[] public observations;
    uint256 public constant MIN_OBSERVATION_WINDOW = 30 minutes;
    uint256 public constant MAX_OBSERVATIONS = 1000;

    event PriceReported(uint256 price, uint256 timestamp);
    event ReporterChanged(address indexed newReporter);

    constructor(address _reporter, uint256 _initialPrice) {
        admin = msg.sender;
        reporter = _reporter;

        // Store price in both locations
        _setNamedPrice(_initialPrice);
        latestPrice = _initialPrice;

        // Initialize TWAP with first observation
        observations.push(Observation({
            timestamp: block.timestamp,
            cumulativePrice: _initialPrice * block.timestamp
        }));
    }

    function getPrice() external view returns (uint256 price) {
        bytes32 slot = PRICE_SLOT;
        assembly {
            price := sload(slot)
        }
    }

    function getLatestPrice() external view returns (uint256) {
        return latestPrice;
    }

    function reportPrice(uint256 price) external {
        require(msg.sender == reporter, "Only reporter");
        require(price > 0, "Price must be positive");

        _setNamedPrice(price);

        latestPrice = price;

        uint256 lastCumulative = observations.length > 0 
            ? observations[observations.length - 1].cumulativePrice 
            : 0;
        uint256 lastTimestamp = observations.length > 0 
            ? observations[observations.length - 1].timestamp 
            : block.timestamp;

        uint256 timeElapsed = block.timestamp - lastTimestamp;
        uint256 newCumulative = lastCumulative + (price * timeElapsed);

        if (observations.length >= MAX_OBSERVATIONS) {
            for (uint256 i = 0; i < observations.length - 1; i++) {
                observations[i] = observations[i + 1];
            }
            observations[observations.length - 1] = Observation({
                timestamp: block.timestamp,
                cumulativePrice: newCumulative
            });
        } else {
            observations.push(Observation({
                timestamp: block.timestamp,
                cumulativePrice: newCumulative
            }));
        }

        emit PriceReported(price, block.timestamp);
    }

    function consultTWAP(uint256 period) external view returns (uint256) {
        require(period >= MIN_OBSERVATION_WINDOW, "Period too short");
        require(observations.length >= 2, "Insufficient observations");

        Observation memory latest = observations[observations.length - 1];
        
        uint256 targetTimestamp = latest.timestamp - period;
        uint256 oldIndex = 0;
        
        for (uint256 i = observations.length - 1; i > 0; i--) {
            if (observations[i].timestamp <= targetTimestamp) {
                oldIndex = i;
                break;
            }
        }

        Observation memory old = observations[oldIndex];
        uint256 timeElapsed = latest.timestamp - old.timestamp;
        
        require(timeElapsed >= MIN_OBSERVATION_WINDOW, "Not enough historical data");
        
        return (latest.cumulativePrice - old.cumulativePrice) / timeElapsed;
    }

    function setReporter(address _reporter) external {
        require(msg.sender == admin, "Only admin");
        reporter = _reporter;
        emit ReporterChanged(_reporter);
    }

    function _setNamedPrice(uint256 price) internal {
        bytes32 slot = PRICE_SLOT;
        assembly {
            sstore(slot, price)
        }
    }
}

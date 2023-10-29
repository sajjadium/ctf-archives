// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

import '@uniswap/v3-core/contracts/libraries/Oracle.sol';

contract MockObservations {
    Oracle.Observation[4] internal oracleObservations;

    int24 slot0Tick;
    uint16 internal slot0ObservationCardinality;
    uint16 internal slot0ObservationIndex;
    uint128 public liquidity;

    bool internal lastObservationCurrentTimestamp;

    constructor(
        uint32[4] memory _blockTimestamps,
        int56[4] memory _tickCumulatives,
        uint128[4] memory _secondsPerLiquidityCumulativeX128s,
        bool[4] memory _initializeds,
        int24 _tick,
        uint16 _observationCardinality,
        uint16 _observationIndex,
        bool _lastObservationCurrentTimestamp,
        uint128 _liquidity
    ) {
        for (uint256 i = 0; i < _blockTimestamps.length; i++) {
            oracleObservations[i] = Oracle.Observation({
                blockTimestamp: _blockTimestamps[i],
                tickCumulative: _tickCumulatives[i],
                secondsPerLiquidityCumulativeX128: _secondsPerLiquidityCumulativeX128s[i],
                initialized: _initializeds[i]
            });
        }

        slot0Tick = _tick;
        slot0ObservationCardinality = _observationCardinality;
        slot0ObservationIndex = _observationIndex;
        lastObservationCurrentTimestamp = _lastObservationCurrentTimestamp;
        liquidity = _liquidity;
    }

    function slot0()
        external
        view
        returns (
            uint160,
            int24,
            uint16,
            uint16,
            uint16,
            uint8,
            bool
        )
    {
        return (0, slot0Tick, slot0ObservationIndex, slot0ObservationCardinality, 0, 0, false);
    }

    function observations(uint256 index)
        external
        view
        returns (
            uint32,
            int56,
            uint160,
            bool
        )
    {
        Oracle.Observation memory observation = oracleObservations[index];
        if (lastObservationCurrentTimestamp) {
            observation.blockTimestamp =
                uint32(block.timestamp) -
                (oracleObservations[slot0ObservationIndex].blockTimestamp - observation.blockTimestamp);
        }
        return (
            observation.blockTimestamp,
            observation.tickCumulative,
            observation.secondsPerLiquidityCumulativeX128,
            observation.initialized
        );
    }
}

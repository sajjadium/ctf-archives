// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.7.6;

contract MockObservable {
    Observation private observation0;
    Observation private observation1;

    struct Observation {
        uint32 secondsAgo;
        int56 tickCumulatives;
        uint160 secondsPerLiquidityCumulativeX128s;
    }

    constructor(
        uint32[] memory secondsAgos,
        int56[] memory tickCumulatives,
        uint160[] memory secondsPerLiquidityCumulativeX128s
    ) {
        require(
            secondsAgos.length == 2 && tickCumulatives.length == 2 && secondsPerLiquidityCumulativeX128s.length == 2,
            'Invalid test case size'
        );

        observation0 = Observation(secondsAgos[0], tickCumulatives[0], secondsPerLiquidityCumulativeX128s[0]);
        observation1 = Observation(secondsAgos[1], tickCumulatives[1], secondsPerLiquidityCumulativeX128s[1]);
    }

    function observe(uint32[] calldata secondsAgos)
        external
        view
        returns (int56[] memory tickCumulatives, uint160[] memory secondsPerLiquidityCumulativeX128s)
    {
        require(
            secondsAgos[0] == observation0.secondsAgo && secondsAgos[1] == observation1.secondsAgo,
            'Invalid test case'
        );

        int56[] memory _tickCumulatives = new int56[](2);
        _tickCumulatives[0] = observation0.tickCumulatives;
        _tickCumulatives[1] = observation1.tickCumulatives;

        uint160[] memory _secondsPerLiquidityCumulativeX128s = new uint160[](2);
        _secondsPerLiquidityCumulativeX128s[0] = observation0.secondsPerLiquidityCumulativeX128s;
        _secondsPerLiquidityCumulativeX128s[1] = observation1.secondsPerLiquidityCumulativeX128s;

        return (_tickCumulatives, _secondsPerLiquidityCumulativeX128s);
    }
}

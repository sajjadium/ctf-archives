// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract SampleEditor {

    enum Align { None, Bars, BarsAndBeats }

    struct Settings {
        Align align;
        bool flexOn;
    }

    struct Region {
        Settings settings;
        bytes data;
    }

    uint256 public project_tempo = 60;
    uint256 public region_tempo = 60;

    mapping(string => Region[]) public tracks;

    error OvO();    // I'm watching you
    error QaQ();

    constructor() {
        Settings memory ff = Settings({align: Align.None, flexOn: false});
        Region[] storage r = tracks["Rhythmic"];
        r.push(Region({settings: ff, data: bytes("part1")}));
        r.push(Region({settings: ff, data: bytes("part2")}));
        r.push(Region({settings: ff, data: bytes("part3")}));
    }

    function setTempo(uint256 _tempo) external {
        if (_tempo > 233) revert OvO();
        project_tempo = _tempo;
    }

    function adjust() external {
        if (!tracks["Rhythmic"][2].settings.flexOn)
            revert QaQ();
        region_tempo = project_tempo;
    }

    function updateSettings(uint256 p, uint256 v) external {
        if (p <= 39) revert OvO();
        assembly {
            sstore(p, v)
        }
    }
}
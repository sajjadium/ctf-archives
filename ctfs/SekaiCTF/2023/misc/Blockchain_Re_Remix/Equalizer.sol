// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";

library LibMath {
    function abs(uint x, uint y) internal pure returns (uint) {
        return x >= y ? x - y : y - x;
    }
}

// ref: https://solidity-by-example.org/defi/stable-swap-amm/
contract Equalizer is ReentrancyGuard {
    using SafeERC20 for IERC20;
    using Address for address payable;

    uint constant private N = 3;
    uint constant private A = 1000 * (N ** (N - 1));

    address[N] public bands;    // frequency bands
    uint[N] public gains;

    uint private constant DECIMALS = 18;
    uint public totalVolumeGain;
    mapping (address => uint) public volumeGainOf;

    error NotConverge(string);
    error Invalid(string);

    constructor(address[N] memory _bands) {
        bands = _bands;
    }

    function _mint(address to, uint gain) internal {
        volumeGainOf[to] += gain;
        totalVolumeGain += gain;
    }

    function _burn(address from, uint gain) internal {
        volumeGainOf[from] -= gain;
        totalVolumeGain -= gain;
    }

    function _getD(uint[N] memory xp) internal pure returns (uint) {
        uint a = A * N;

        uint s;
        for (uint i; i < N; ++i) {
            s += xp[i];
        }

        uint d = s;
        uint d_prev;
        for (uint i; i < 255; ++i) {
            uint p = d;
            for (uint j; j < N; ++j) {
                p = (p * d) / (N * xp[j]);
            }
            d_prev = d;
            d = ((a * s + N * p) * d) / ((a - 1) * d + (N + 1) * p);

            if (LibMath.abs(d, d_prev) <= 1) {
                return d;
            }
        }
        revert NotConverge("D");
    }

    function _getY(
        uint i,
        uint j,
        uint x,
        uint[N] memory xp
    ) internal pure returns (uint) {
        uint a = A * N;
        uint d = _getD(xp);
        uint s;
        uint c = d;

        uint _x;
        for (uint k; k < N; ++k) {
            if (k == i) {
                _x = x;
            } else if (k == j) {
                continue;
            } else {
                _x = xp[k];
            }

            s += _x;
            c = (c * d) / (N * _x);
        }
        c = (c * d) / (N * a);
        uint b = s + d / a;

        uint y_prev;
        uint y = d;
        for (uint _i; _i < 255; ++_i) {
            y_prev = y;
            y = (y * y + c) / (2 * y + b - d);
            if (LibMath.abs(y, y_prev) <= 1) {
                return y;
            }
        }
        revert NotConverge("Y");
    }

    function getGlobalInfo() external view returns (uint) {
        uint d = _getD(gains);
        uint _totalVolumeGain = totalVolumeGain;
        if (_totalVolumeGain > 0) {
            return (d * 10 ** DECIMALS) / _totalVolumeGain;
        }
        return 0;
    }

    /**
     * @param i index of the band to boost
     * @param j index of the band to cut
     * @param dx determines the magnitude of the boost
     * @return dy determines the magnitude of the cut
     */
    function equalize(uint i, uint j, uint dx)
        external
        payable
        nonReentrant
        returns (uint dy) {
        if (i == j)
            revert Invalid("index");
        if (dx == 0)
            revert Invalid("dx");

        if (i == 0) {
            if (msg.value != dx)
                revert Invalid("value");
        } else {
            if (msg.value != 0)
                revert Invalid("value");
            IERC20(bands[i]).safeTransferFrom(msg.sender, address(this), dx);
        }

        uint[N] memory xp = gains;
        uint x = xp[i] + dx;

        uint y0 = xp[j];
        uint y1 = _getY(i, j, x, xp);
        dy = y0 - y1 - 1;

        gains[i] += dx;
        gains[j] -= dy;

        if (j == 0) {
            payable(msg.sender).sendValue(dy);
        } else {
            IERC20(bands[j]).safeTransfer(msg.sender, dy);
        }
    }

    function increaseVolume(
        uint[N] calldata amounts
    ) payable external nonReentrant returns (uint variation) {
        uint _totalVolumeGain = totalVolumeGain;
        uint d0;
        uint[N] memory old_xs = gains;
        if (_totalVolumeGain > 0) {
            d0 = _getD(old_xs);
        }

        uint[N] memory new_xs;
        for (uint i; i < N; ++i) {
            uint amount = amounts[i];
            if (amount > 0) {
                if (i == 0) {
                    require(msg.value == amount);
                } else {
                    IERC20(bands[i]).safeTransferFrom(msg.sender, address(this), amount);
                }
                new_xs[i] = old_xs[i] + amount;
            } else {
                new_xs[i] = old_xs[i];
            }
        }

        uint d1 = _getD(new_xs);
        if (d1 <= d0)
            revert Invalid("not increase");

        // update
        for (uint i; i < N; ++i) {
            gains[i] += amounts[i];
        }

        if (_totalVolumeGain > 0) {
            variation = ((d1 - d0) * _totalVolumeGain) / d0;
        } else {
            variation = d1;
        }
        _mint(msg.sender, variation);
    }

    function decreaseVolume(
        uint variation
    ) external nonReentrant returns (uint[N] memory amounts) {
        if (variation == 0)
            revert Invalid("variation");
        uint _totalVolumeGain = totalVolumeGain;

        for (uint i; i < N; ++i) {
            uint amount = (variation * gains[i]) / _totalVolumeGain;
            gains[i] -= amount;
            amounts[i] = amount;

            if (i == 0) {
                payable(msg.sender).sendValue(amount);
            } else {
                IERC20(bands[i]).safeTransfer(msg.sender, amount);
            }
        }

        _burn(msg.sender, variation);
    }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./TimekeeperToken.sol";
import "./TimekeeperOracle.sol";
import "./TimekeeperProxy.sol";
import "./TimekeeperLending.sol";
import "./TimekeeperGovernance.sol";

/**
 * @title Setup
 * @notice Deployment contract for "The Timekeeper's Paradox" challenge.
 *         Deploys the full DeFi ecosystem:
 *         - TKG governance token
 *         - Price oracle with TWAP
 *         - Upgradeable proxy (wrapping oracle)
 *         - Lending pool
 *         - Governance
 *
 *         The challenge is solved when the lending pool is drained of all ETH.
 */
contract Setup {
    TimekeeperToken public token;
    TimekeeperOracle public oracle;
    TimekeeperProxy public proxy;
    TimekeeperLending public lending;
    TimekeeperGovernance public governance;

    constructor(address _player) payable {
        require(msg.value >= 50 ether, "Need 50 ETH");

        // 1. Deploy governance token
        //    Deployer gets 900,000 TKG (90%) — governance quorum unreachable for player
        token = new TimekeeperToken(900_000 * 1e18);

        // 2. Deploy oracle with initial price: 1000 TKG per ETH
        oracle = new TimekeeperOracle(address(this), 1000 * 1e18);

        // 3. Deploy proxy wrapping the oracle (using CREATE2 for predictable address)
        bytes32 salt = keccak256("timekeeper-proxy-v1");
        proxy = new TimekeeperProxy{salt: salt}(address(oracle));

        // 4. Deploy lending pool using the PROXY address as oracle
        lending = new TimekeeperLending(address(token), address(proxy));

        // 5. Deploy governance
        governance = new TimekeeperGovernance(
            address(token),
            address(proxy),
            address(lending)
        );

        // 6. Fund the lending pool with all ETH
        (bool success, ) = address(lending).call{value: msg.value}("");
        require(success, "Failed to fund lending pool");

        // 7. Send tokens to the lending pool for borrowing
        token.transfer(address(lending), 500_000 * 1e18);

        // 8. Give player 10,000 TKG tokens (1% — not enough for governance)
        token.mint(_player, 10_000 * 1e18);
    }

    /**
     * @notice Check if the challenge is solved
     * @return True if the lending pool has been drained of all ETH
     */
    function isSolved() external view returns (bool) {
        return address(lending).balance == 0;
    }
}

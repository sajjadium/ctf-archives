// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import {AppStorage, Checkpoint, LibAppStorage} from "../libraries/LibAppStorage.sol";
// import { LibERC20 } from "../libraries/LibERC20.sol";
import {LibDiamond} from "../libraries/LibDiamond.sol";
import {ECDSA} from "../libraries/ECDSA.sol";

import {LibDAO} from "../libraries/LibDAO.sol";

contract FeatherCoinFacet {
    AppStorage internal s;

    /*//////////////////////////////////////////////////////////////
                               READ FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    function name() external pure returns (string memory) {
        return "FeatherCoin";
    }

    function symbol() external pure returns (string memory) {
        return "FTC";
    }

    function decimals() external pure returns (uint8) {
        return 18;
    }

    function totalSupply() public view returns (uint256) {
        return s.totalSupply;
    }

    function balanceOf(address _account) external view returns (uint256) {
        return s.balances[_account];
    }

    function allowance(address _account, address _spender) external view returns (uint256) {
        return s.allowances[_account][_spender];
    }

    /*//////////////////////////////////////////////////////////////
                               TOKEN LOGIC
    //////////////////////////////////////////////////////////////*/

    function mint(address _to, uint256 _amount) external {
        LibDiamond.enforceIsContractOwner();
        _mint(_to, _amount);

        _moveDelegates(address(0), s.delegates[_to], _amount);
    }

    function approve(address _spender, uint256 _amount) external returns (bool) {
        s.allowances[msg.sender][_spender] = _amount;

        return true;
    }

    function transfer(address _to, uint256 _amount) external returns (bool) {
        s.balances[msg.sender] -= _amount;

        unchecked {
            s.balances[_to] += _amount;
        }

        _moveDelegates(s.delegates[msg.sender], s.delegates[_to], _amount);

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _amount) external returns (bool) {
        uint256 allowed = s.allowances[_from][msg.sender];

        if (allowed != type(uint256).max) {
            s.allowances[_from][msg.sender] = allowed - _amount;
        }

        s.balances[_from] -= _amount;

        unchecked {
            s.balances[_to] += _amount;
        }

        _moveDelegates(s.delegates[_from], s.delegates[_to], _amount);

        return true;
    }

    /*//////////////////////////////////////////////////////////////
                        DELEGATE LOGIC
    //////////////////////////////////////////////////////////////*/

    function delegate(address _delegatee) public {
        return _delegate(msg.sender, _delegatee);
    }

    function getCurrentVotes(address _account) external view returns (uint256) {
        return LibDAO.getCurrentVotes(_account);
    }

    function getNumberOfCheckpoints(address _account) external view returns (uint32) {
        return s.numCheckpoints[_account];
    }

    function getCheckpoint(address _account, uint32 _pos) external view returns (Checkpoint memory) {
        return s.checkpoints[_account][_pos];
    }

    function getPriorVotes(address _account, uint256 _blockNumber) public view returns (uint256) {
        return LibDAO.getPriorVotes(_account, _blockNumber);
    }

    function _delegate(address _delegator, address _delegatee) internal {
        address currentDelegate = s.delegates[_delegator];
        uint256 delegatorBalance = s.balances[_delegator];

        s.delegates[_delegator] = _delegatee;

        _moveDelegates(currentDelegate, _delegatee, delegatorBalance);
    }

    function _moveDelegates(address _src, address _dst, uint256 _amount) internal {
        if (_src != _dst && _amount > 0) {
            if (_src != address(0)) {
                uint32 srcRepNum = s.numCheckpoints[_src];
                uint256 srcRepOld = srcRepNum > 0 ? s.checkpoints[_src][srcRepNum - 1].votes : 0;
                uint256 srcRepNew = srcRepOld - _amount;

                _writeCheckpoint(_src, srcRepNum, srcRepOld, srcRepNew);
            }

            if (_dst != address(0)) {
                uint32 dstRepNum = s.numCheckpoints[_dst];
                uint256 dstRepOld = dstRepNum > 0 ? s.checkpoints[_dst][dstRepNum - 1].votes : 0;
                uint256 dstRepNew = dstRepOld + _amount;

                _writeCheckpoint(_dst, dstRepNum, dstRepOld, dstRepNew);
            }
        }
    }

    function _writeCheckpoint(address _delegatee, uint32 _nCheckpoints, uint256, /* _oldVotes */ uint256 _newVotes)
        internal
    {
        uint32 blockNumber = safe32(block.number, "FTC: block number exceeds 32 bits");

        if (_nCheckpoints > 0 && s.checkpoints[_delegatee][_nCheckpoints - 1].fromBlock == blockNumber) {
            s.checkpoints[_delegatee][_nCheckpoints - 1].votes = _newVotes;
        } else {
            s.checkpoints[_delegatee][_nCheckpoints] = Checkpoint(blockNumber, _newVotes);
            s.numCheckpoints[_delegatee] = _nCheckpoints + 1;
        }
    }

    /*//////////////////////////////////////////////////////////////
                        MINT / BURN LOGIC
    //////////////////////////////////////////////////////////////*/

    function _mint(address _to, uint256 _amount) internal {
        s.totalSupply += _amount;

        unchecked {
            s.balances[_to] += _amount;
        }
    }

    function _burn(address _from, uint256 _amount) internal {
        s.balances[_from] -= _amount;

        unchecked {
            s.totalSupply -= _amount;
        }
    }

    /*//////////////////////////////////////////////////////////////
                        INTERNAL UTILS
    //////////////////////////////////////////////////////////////*/

    function safe32(uint256 _number, string memory _errorMessage) internal pure returns (uint32) {
        require(_number < 2 ** 32, _errorMessage);
        return uint32(_number);
    }
}

pragma solidity >=0.8.0 <0.9.0;

uint256 constant SMT_STACK_SIZE = 32;
uint256 constant DEPTH = 160;

library SMT {
    struct Leaf {
        address key;
        uint8 value;
    }

    enum Mode {
        BlackList,
        WhiteList
    }

    enum Method {
        Insert,
        Delete
    }

    function init() internal pure returns (bytes32) {
        return 0;
    }

    function calcLeaf(Leaf memory a) internal pure returns (bytes32) {
        if (a.value == 0) {
            return 0;
        } else {
            return keccak256(abi.encode(a.key, a.value));
        }
    }

    function merge(bytes32 l, bytes32 r) internal pure returns (bytes32) {
        if (l == 0) {
            return r;
        } else if (r == 0) {
            return l;
        } else {
            return keccak256(abi.encode(l, r));
        }
    }

    function verifyByMode(
        bytes32[] memory _proofs,
        address[] memory _targets,
        bytes32 _expectedRoot,
        Mode _mode
    ) internal pure returns (bool) {
        Leaf[] memory leaves = new Leaf[](_targets.length);
        for (uint256 i = 0; i < _targets.length; i++) {
            leaves[i] = Leaf({key: _targets[i], value: uint8(_mode)});
        }
        return verify(_proofs, leaves, _expectedRoot);
    }

    function verify(
        bytes32[] memory _proofs,
        Leaf[] memory _leaves,
        bytes32 _expectedRoot
    ) internal pure returns (bool) {
        return (calcRoot(_proofs, _leaves, _expectedRoot) == _expectedRoot);
    }

    function updateSingleTarget(
        bytes32[] memory _proofs,
        address _target,
        bytes32 _prevRoot,
        Method _method
    ) internal pure returns (bytes32) {
        Leaf[] memory nextLeaves = new Leaf[](1);
        Leaf[] memory prevLeaves = new Leaf[](1);
        nextLeaves[0] = Leaf({key: _target, value: uint8(_method) ^ 1});
        prevLeaves[0] = Leaf({key: _target, value: uint8(_method)});
        return update(_proofs, nextLeaves, prevLeaves, _prevRoot);
    }
    function unpdateTargets(
        bytes32[] memory _proofs,
        address[] memory _targets,
        bytes32 _prevRoot,
        Method _method
    ) internal pure returns (bytes32){
        Leaf[] memory nextLeaves = new Leaf[](_targets.length);
        Leaf[] memory prevLeaves = new Leaf[](_targets.length);
        
        for(uint256 i = 0;i<_targets.length;i++){
            nextLeaves[i] = Leaf({key: _targets[i], value: uint8(_method) ^ 1});
            prevLeaves[i] = Leaf({key: _targets[i], value: uint8(_method)});
        }
        return update(_proofs, nextLeaves, prevLeaves, _prevRoot);
    }
    function update(
        bytes32[] memory _proofs,
        Leaf[] memory _nextLeaves,
        Leaf[] memory _prevLeaves,
        bytes32 _prevRoot
    ) internal pure returns (bytes32) {
        require(verify(_proofs, _prevLeaves, _prevRoot), "update proof not valid");
        return calcRoot(_proofs, _nextLeaves, _prevRoot);
    }

    function checkGroupSorted(Leaf[] memory _leaves) internal pure returns (bool) {
        require(_leaves.length >= 1);
        uint160 temp = 0;
        for (uint256 i = 0; i < _leaves.length; i++) {
            if (temp >= uint160(_leaves[i].key)) {
                return false;
            }
            temp = uint160(_leaves[i].key);
        }
        return true;
    }

    function getBit(uint160 key, uint256 height) internal pure returns (uint256) {
        require(height <= DEPTH);
        return (key >> height) & 1;
    }

    function parentPath(uint160 key, uint256 height) internal pure returns (uint160) {
        require(height <= DEPTH);
        return copyBit(key, height + 1);
    }

    function copyBit(uint160 key, uint256 height) internal pure returns (uint160) {
        require(height <= DEPTH);
        return ((key >> height) << height);
    }

    function calcRoot(
        bytes32[] memory _proofs,
        Leaf[] memory _leaves,
        bytes32 _root
    ) internal pure returns (bytes32) {
        require(checkGroupSorted(_leaves));
        uint160[] memory stackKeys = new uint160[](SMT_STACK_SIZE);
        bytes32[] memory stackValues = new bytes32[](SMT_STACK_SIZE);
        uint256 proofIndex = 0;
        uint256 leaveIndex = 0;
        uint256 stackTop = 0;

        while (proofIndex < _proofs.length) {
            if (uint256(_proofs[proofIndex]) == 0x4c) {
                proofIndex++;
                require(stackTop < SMT_STACK_SIZE);
                require(leaveIndex < _leaves.length);
                stackKeys[stackTop] = uint160(_leaves[leaveIndex].key);
                stackValues[stackTop] = calcLeaf(_leaves[leaveIndex]);
                stackTop++;
                leaveIndex++;
            } else if (uint256(_proofs[proofIndex]) == 0x50) {
                proofIndex++;
                require(stackTop != 0);
                require(proofIndex + 2 <= _proofs.length);

                uint256 height = uint256(_proofs[proofIndex++]);
                bytes32 currentProof = _proofs[proofIndex++];
                require(currentProof != _root);
                if (getBit(stackKeys[stackTop - 1], height) == 1) {
                    stackValues[stackTop - 1] = merge(currentProof, stackValues[stackTop - 1]);
                } else {
                    stackValues[stackTop - 1] = merge(stackValues[stackTop - 1], currentProof);
                }
                stackKeys[stackTop - 1] = parentPath(stackKeys[stackTop - 1], height);
            } else if (uint256(_proofs[proofIndex]) == 0x48) {
                proofIndex++;
                require(stackTop >= 2);
                require(proofIndex < _proofs.length);
                uint256 height = uint256(_proofs[proofIndex++]);
                uint256 aSet = getBit(stackKeys[stackTop - 2], height);
                uint256 bSet = getBit(stackKeys[stackTop - 1], height);
                stackKeys[stackTop - 2] = parentPath(stackKeys[stackTop - 2], height);
                stackKeys[stackTop - 1] = parentPath(stackKeys[stackTop - 1], height);
                require(stackKeys[stackTop - 2] == stackKeys[stackTop - 1] && aSet != bSet);

                if (aSet == 1) {
                    stackValues[stackTop - 2] = merge(
                        stackValues[stackTop - 1],
                        stackValues[stackTop - 2]
                    );
                } else {
                    stackValues[stackTop - 2] = merge(
                        stackValues[stackTop - 2],
                        stackValues[stackTop - 1]
                    );
                }
                stackTop -= 1;
            } else {
                revert();
            }
        }
        require(leaveIndex == _leaves.length);
        require(stackTop == 1);
        return stackValues[0];
    }
}


contract TreasureHunter {
    bytes32 public root;
    SMT.Mode public smtMode = SMT.Mode.WhiteList;
    bool public solved = false;
    address[] team;

    mapping(address => bool) public haveKey;
    mapping(address => bool) public haveTreasureChest;

    event FindKey(address indexed _from);
    event PickupTreasureChest(address indexed _from);
    event OpenTreasureChest(address indexed _from);

    constructor() public {
        root = SMT.init();
        _init();
    }

    function _init() internal {
        address[] memory hunters = new address[](8);
        hunters[0] = 0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e;
        hunters[1] = 0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45;
        hunters[2] = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
        hunters[3] = 0x6B3595068778DD592e39A122f4f5a5cF09C90fE2;
        hunters[4] = 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B;
        hunters[5] = 0xc00e94Cb662C3520282E6f5717214004A7f26888;
        hunters[6] = 0xD533a949740bb3306d119CC777fa900bA034cd52;
        hunters[7] = 0xdAC17F958D2ee523a2206206994597C13D831ec7;

        SMT.Leaf[] memory nextLeaves = new SMT.Leaf[](8);
        SMT.Leaf[] memory prevLeaves = new SMT.Leaf[](8);
        for (uint8 i = 0; i < hunters.length; i++) {
            nextLeaves[i] = SMT.Leaf({key: hunters[i], value: 1});
            prevLeaves[i] = SMT.Leaf({key: hunters[i], value: 0});
        }

        bytes32[] memory proof = new bytes32[](22);
        proof[0] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[1] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[2] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[3] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[4] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[5] = 0x0000000000000000000000000000000000000000000000000000000000000095;
        proof[6] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[7] = 0x0000000000000000000000000000000000000000000000000000000000000099;
        proof[8] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[9] = 0x000000000000000000000000000000000000000000000000000000000000009e;
        proof[10] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[11] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[12] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[13] = 0x000000000000000000000000000000000000000000000000000000000000004c;
        proof[14] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[15] = 0x000000000000000000000000000000000000000000000000000000000000009b;
        proof[16] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[17] = 0x000000000000000000000000000000000000000000000000000000000000009c;
        proof[18] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[19] = 0x000000000000000000000000000000000000000000000000000000000000009e;
        proof[20] = 0x0000000000000000000000000000000000000000000000000000000000000048;
        proof[21] = 0x000000000000000000000000000000000000000000000000000000000000009f;

        root = SMT.update(proof, nextLeaves, prevLeaves, root);
    }
    function checkteam() public returns (bool){
        for(uint i = 0;i<team.length;i++){
            if(team[i] == msg.sender){
                return false;
            }
        }
        return true;
    }

    function removeIndex(uint index) internal returns (address[] memory){
        require(index < team.length);
        for(uint i = index;i<team.length-1;i++){
            team[i] = team[i+1];
        }
        team.pop();
        return team;
    }
    function enter(bytes32[] memory _proofs) public {
        require(haveKey[msg.sender] == false);
        require(checkteam());
        team.push(msg.sender);
        root = SMT.updateSingleTarget(_proofs, msg.sender, root, SMT.Method.Insert);
    }

    function leave(bytes32[] memory _proofs) public {
        require(haveTreasureChest[msg.sender] == false);
        for(uint i = 0;i<team.length;i++){
            if(team[i] == msg.sender){
                team = removeIndex(i);
            }
        }
        root = SMT.updateSingleTarget(_proofs, msg.sender, root, SMT.Method.Delete);
    }

    function findKey(bytes32[] memory _proofs) public {
        require(smtMode == SMT.Mode.BlackList, "not blacklist mode");
        require(team.length >= 4);
        require(SMT.verifyByMode(_proofs, team, root, smtMode), "hunter has fallen into a trap");
        haveKey[msg.sender] = true;
        smtMode = SMT.Mode.WhiteList;
        emit FindKey(msg.sender);
    }

    function pickupTreasureChest(bytes32[] memory _proofs) public {
        require(smtMode == SMT.Mode.WhiteList, "not whitelist mode");
        require(team.length >= 4);
        require(
            SMT.verifyByMode(_proofs, team, root, smtMode),
            "hunter hasn't found the treasure chest"
        );
        haveTreasureChest[msg.sender] = true;
        smtMode = SMT.Mode.BlackList;
        emit PickupTreasureChest(msg.sender);
    }

    function openTreasureChest() public {
        require(haveKey[msg.sender] && haveTreasureChest[msg.sender]);
        solved = true;
        emit OpenTreasureChest(msg.sender);
    }

    function isSolved() public view returns (bool) {
        return solved;
    }
}

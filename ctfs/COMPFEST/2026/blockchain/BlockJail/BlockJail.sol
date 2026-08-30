// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

contract BlockJail {
    error InvalidAgent();
    error HeartLocked();

    uint256 public constant MAX_AGENT_SIZE = 36;
    address public immutable PALACE;
    address public agent;
    address public beneficiary;
    bool public pathOpened;

    modifier onlyAgent() {
        if (msg.sender != agent) revert InvalidAgent();
        _;
    }

    constructor(address palace) payable {
        if (palace.code.length == 0) revert InvalidAgent();
        PALACE = palace;
    }

    function enter() external {
        if (agent != address(0) || msg.sender.code.length == 0) revert InvalidAgent();
        _validateAgentRuntime(msg.sender);
        agent = msg.sender;
        beneficiary = tx.origin;
    }

    function openPath() external onlyAgent {
        pathOpened = true;
    }

    function stealHeart() external onlyAgent {
        if (!pathOpened) revert HeartLocked();
        (bool ok,) = payable(beneficiary).call{value: address(this).balance}("");
        if (!ok) revert HeartLocked();
    }

    function infiltrate(bytes calldata card) external onlyAgent returns (bytes memory) {
        if (!pathOpened) revert HeartLocked();
        (bool ok, bytes memory result) = PALACE.call(
            abi.encodeWithSignature("beginInfiltration(bytes)", card)
        );
        if (!ok) {
            assembly {
                revert(add(result, 0x20), mload(result))
            }
        }
        return result;
    }

    function _validateAgentRuntime(address candidate) internal view {
        bytes memory code = candidate.code;
        if (code.length == 0 || code.length > MAX_AGENT_SIZE) revert InvalidAgent();

        uint256 delegatecalls;
        bool hasVanityImplementation;
        uint256 i;
        while (i < code.length) {
            uint8 opcode = uint8(code[i]);
            if (opcode >= 0x60 && opcode <= 0x7f) {
                uint256 pushSize = opcode - 0x5f;
                if (i + pushSize >= code.length) revert InvalidAgent();
                if (pushSize <= 20) {
                    uint160 operand;
                    for (uint256 j; j < pushSize; ++j) {
                        operand = (operand << 8) | uint8(code[i + 1 + j]);
                    }
                    if (
                        operand <= type(uint144).max
                            && address(operand).code.length != 0
                    ) hasVanityImplementation = true;
                }
                i += 1 + pushSize;
                continue;
            }
            if (!_isAllowed(opcode)) revert InvalidAgent();
            if (opcode == 0xf4) ++delegatecalls;
            ++i;
        }

        if (delegatecalls != 1 || !hasVanityImplementation) revert InvalidAgent();
    }

    function _isAllowed(uint8 opcode) internal pure returns (bool) {
        if (
            opcode == 0x00 || opcode == 0x36 || opcode == 0x37 || opcode == 0x3d
                || opcode == 0x3e || opcode == 0x50 || opcode == 0x5a
                || opcode == 0x5f || opcode == 0xf3 || opcode == 0xf4
                || opcode == 0xfd
        ) return true;
        return opcode >= 0x80 && opcode <= 0x9f;
    }

    receive() external payable {}
}

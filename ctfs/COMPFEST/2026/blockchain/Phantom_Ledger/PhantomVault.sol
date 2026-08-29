// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PhantomVault {
    address public owner;
    address public relayer;
    address public feeRecipient;

    uint256 public feeRate;
    uint256 public constant MAX_FEE_RATE = 500;

    mapping(address => uint256) public balances;
    mapping(bytes32 => bool) public usedSignatures;

    uint256 private _locked;

    address public proposedRelayer;
    uint256 public relayerChangeTimestamp;
    uint256 public constant RELAYER_CHANGE_DELAY = 1 hours;

    event Deposit(address indexed user, uint256 amount);
    event Withdraw(address indexed user, uint256 amount);
    event RelayedWithdraw(address indexed signer, address indexed to, uint256 amount, uint256 fee);
    event CreditTransfer(address indexed from, address indexed to, uint256 amount);
    event FeeRateUpdated(uint256 newRate);
    event RelayerProposed(address indexed proposed);
    event RelayerChanged(address indexed newRelayer);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyRelayer() {
        require(msg.sender == relayer, "Not relayer");
        _;
    }

    modifier nonReentrant() {
        require(_locked == 0, "Reentrancy detected");
        _locked = 1;
        _;
        _locked = 0;
    }

    constructor(address _relayer, address _feeRecipient) payable {
        owner = msg.sender;
        relayer = _relayer;
        feeRecipient = _feeRecipient;
        feeRate = 200;
        _locked = 0;

        if (msg.value > 0) {
            balances[msg.sender] += msg.value;
            emit Deposit(msg.sender, msg.value);
        }
    }

    function deposit() external payable {
        require(msg.value > 0, "Zero deposit");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "ETH transfer failed");
        emit Withdraw(msg.sender, amount);
    }

    function relayWithdraw(
        address to,
        uint256 amount,
        uint256 nonce,
        bytes memory signature
    ) external onlyRelayer nonReentrant {
        bytes32 sigHash = keccak256(signature);
        require(!usedSignatures[sigHash], "Signature already used");

        bytes32 messageHash = keccak256(
            abi.encodePacked(
                "\x19Ethereum Signed Message:\n32",
                keccak256(abi.encodePacked(to, amount, nonce, address(this)))
            )
        );

        address signer = _recoverSigner(messageHash, signature);
        require(signer != address(0), "Invalid signature");
        require(balances[signer] >= amount, "Insufficient signer balance");

        usedSignatures[sigHash] = true;

        uint256 fee;
        unchecked {
            fee = (amount * feeRate) / 10000;
        }
        uint256 netAmount = amount - fee;

        balances[signer] -= amount;
        if (fee > 0 && feeRecipient != address(0)) {
            (bool feeSuccess, ) = payable(feeRecipient).call{value: fee}("");
            require(feeSuccess, "Fee transfer failed");
        }

        (bool success, ) = payable(to).call{value: netAmount}("");
        require(success, "Withdrawal transfer failed");

        emit RelayedWithdraw(signer, to, amount, fee);
    }

    function transferCredit(address from, address to, uint256 amount) external {
        require(msg.sender == from || msg.sender == relayer, "Not authorized");
        require(balances[from] >= amount, "Insufficient credit");

        balances[from] -= amount;
        balances[to] += amount;

        emit CreditTransfer(from, to, amount);
    }

    function setFeeRate(uint256 newRate) external onlyOwner {
        require(newRate <= MAX_FEE_RATE, "Fee rate exceeds maximum");
        feeRate = newRate;
        emit FeeRateUpdated(newRate);
    }

    function proposeRelayer(address _newRelayer) external onlyOwner {
        require(_newRelayer != address(0), "Invalid relayer");
        proposedRelayer = _newRelayer;
        relayerChangeTimestamp = block.timestamp;
        emit RelayerProposed(_newRelayer);
    }

    function confirmRelayerChange() external {
        require(msg.sender == relayer, "Only current relayer");
        require(proposedRelayer != address(0), "No pending proposal");
        require(
            block.timestamp <= relayerChangeTimestamp + RELAYER_CHANGE_DELAY,
            "Proposal expired"
        );
        relayer = proposedRelayer;
        proposedRelayer = address(0);
        relayerChangeTimestamp = 0;
        emit RelayerChanged(relayer);
    }

    function setFeeRecipient(address _feeRecipient) external {
        require(msg.sender == owner || msg.sender == relayer, "Not authorized");
        feeRecipient = _feeRecipient;
    }

    function _recoverSigner(
        bytes32 hash,
        bytes memory sig
    ) internal pure returns (address) {
        require(sig.length == 65, "Invalid signature length");
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
        if (v < 27) { v += 27; }
        require(v == 27 || v == 28, "Invalid v value");
        return ecrecover(hash, v, r, s);
    }

    function getBalance(address account) external view returns (uint256) {
        return balances[account];
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}

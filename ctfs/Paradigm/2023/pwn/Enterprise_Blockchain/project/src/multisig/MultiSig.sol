pragma solidity 0.8.15;

contract SimpleMultiSigGov {
    address constant ADMIN = address(1337);
    address o0;
    address o1;
    address o2;

    uint64 REQUIRED_GAS = 2000;

    modifier onlyMultiSig() {
        require(msg.sender == address(this), "OMS");
        _;
    }

    constructor(address owner0, address owner1, address owner2) {
        o0 = owner0;
        o1 = owner1;
        o2 = owner2;
    }

    function execTransaction(
        address to,
        bytes memory data,
        uint8[3] calldata vs,
        bytes32[3] calldata rs,
        bytes32[3] calldata ss
    ) external {
        bytes32 hash = sha256(abi.encodePacked(keccak256(abi.encodePacked(to, data))));

        uint8 cnt = 0;
        cnt = ecrecover(hash, vs[0], rs[0], ss[0]) == o0 ? cnt + 1 : cnt;
        cnt = ecrecover(hash, vs[1], rs[1], ss[1]) == o1 ? cnt + 1 : cnt;
        cnt = ecrecover(hash, vs[2], rs[2], ss[2]) == o2 ? cnt + 1 : cnt;

        require(cnt >= 2, "ETS");

        (bool success,) = address(to).call(data);
        require(success, "ETF");
    }

    function emergencyStop() external onlyMultiSig {
        (bool success,) = ADMIN.staticcall{gas: 2000}(hex"01");
    }

    function reloadConfig(uint8 _type, bytes memory data) external onlyMultiSig {
        if (_type == 1) {
            address newAdmin = abi.decode(data, (address));
            (bool success,) = ADMIN.staticcall{gas: 2000}(abi.encodePacked(hex"0201", newAdmin));
        } else if (_type == 2) {
            uint64 requiredGas = abi.decode(data, (uint64));
            (bool success,) = ADMIN.staticcall{gas: 2000}(abi.encodePacked(hex"0202", requiredGas));
        } else if (_type == 3) {
            return;
        } else if (_type == 4) {
            (bool success,) = ADMIN.staticcall{gas: 2000}(abi.encodePacked(hex"0204", data));
        }
    }
}

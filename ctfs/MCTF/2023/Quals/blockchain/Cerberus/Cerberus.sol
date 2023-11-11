// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.21;


contract Cerberus {
    bytes32 private password;
    bytes12 private secretKey1;
    uint152 private secretKey2;
    bool private secretKey3;
    bool public solved;

    constructor(
                bytes32 _password, 
                bytes12 _secretKey1, 
                uint152 _secretKey2, 
                bool _secretKey3
                ) 
    {
        password = _password;
        secretKey1 = _secretKey1;
        secretKey2 = _secretKey2;
        secretKey3 = _secretKey3;
    }

    modifier firstHead(bytes32 _password, uint256 _secret) {
        uint160 secret;
        require(_password == password, "Password is incorrect!");
        assembly {
            secret := sload(1)
        }
        require(_secret == secret, "Secret is incorrect!");
        _;
    }
    

    modifier secondHead {
        uint256 size;
        require(tx.origin != msg.sender, "EOA not allowed!");
        assembly {
            size := extcodesize(caller())
        }
        require(size == 0, "Smart Contract not allowed!");
        _;
    }

    modifier thirdHead(address sword) { 
        (bool success, ) = sword.delegatecall(abi.encodeWithSignature("finalBlow()"));
        require(success, "Call failed!");
        _;
    }

    function fightTheCerberus(bytes32 _password, uint256 _secret, address sword) 
        firstHead(_password, _secret)
        secondHead
        thirdHead(sword)
        external 
        returns (string memory)
    {
        if (solved) {
            return "You did it!";
        } else {
            return "Cerberus still alive...";
        }
    }

}

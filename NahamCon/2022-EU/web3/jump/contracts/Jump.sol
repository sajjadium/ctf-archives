pragma solidity 0.8.17;

contract Jump {

    constructor() payable { require(msg.value != 0); }

    function withdraw() private {
        require(msg.value == 0, 'dont send funds!');
        payable(msg.sender).transfer(address(this).balance);
    }

    function frwd() internal
        { withdraw(); }

    struct Func { function () internal f; }

    function breakIt() public payable {
        require(msg.value != 0, 'send funds!');
        Func memory func;
        func.f = frwd;
        assembly { mstore(func, add(mload(func), callvalue())) }
        func.f();
    }
}

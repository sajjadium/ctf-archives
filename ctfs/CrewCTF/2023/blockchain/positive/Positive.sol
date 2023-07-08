// SPDX-License-Identifier: MIT
pragma solidity =0.7.6;

contract Positive{
    bool public solved;

    constructor() {
        solved = false;
    }

    function stayPositive(int64 _num) public returns(int64){
        int64 num;
        if(_num<0){
            num = -_num;
            if(num<0){
                solved = true;
            }
            return num;
        }
        num = _num;
        return num;
    }

}
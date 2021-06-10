pragma solidity ^0.6.0;

contract crack_me{

    function gib_flag(uint arg1, string memory arg2, uint arg3) public view returns (uint[]){
        //arg3 is a overflow
        require(arg3 > 0, "positive nums only baby");
        if ((arg1 ^ 0x70) == 20) {
            if(keccak256(bytes(decrypt(arg2))) == keccak256(bytes("offshift ftw"))) {
                uint256 check3 = arg3 + 1;
                if( check3< 1) {
                    return flag;
                }
            }
        }
        return "you lost babe";
    }

    function decrypt(string memory encrypted_text) private pure returns (string memory){
        uint256 length = bytes(encrypted_text).length;
        for (uint i = 0; i < length; i++) {
            byte char = bytes(encrypted_text)[i];
            assembly {
                char := byte(0,char)
                if and(gt(char,0x60), lt(char,0x6E))
                { char:= add(0x7B, sub(char,0x61)) }
                if iszero(eq(char, 0x20))
                {mstore8(add(add(encrypted_text,0x20), mul(i,1)), sub(char,16))}
            }
        }
        return encrypted_text;
    }
}

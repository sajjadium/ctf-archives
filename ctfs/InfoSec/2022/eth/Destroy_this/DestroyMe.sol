pragma solidity 0.7.0;

contract DestroyMe {
    function run(address code) external payable {
        assembly {
            if eq(caller(), address()) {
                switch delegatecall(gas(), code, 0x00, 0x00, 0x00, 0x00)
                    case 0 {
                        returndatacopy(0x00, 0x00, returndatasize())
                        revert(0x00, returndatasize())
                    }
                    case 1 {
                        returndatacopy(0x00, 0x00, returndatasize())
                        return(0x00, returndatasize())
                    }
            }
            
            if lt(gas(), 0xf000) {
                revert(0x00, 0x00)
            }
            
            calldatacopy(0x00, 0x00, calldatasize())
            
    
            if iszero(staticcall(0x4000, address(), 0, calldatasize(), 0, 0)) {
                revert(0x00, 0x00)
            }
            
        
            switch call(0x4000, address(), 0, 0, calldatasize(), 0, 0)
                case 0 {
                    returndatacopy(0x00, 0x00, returndatasize())
                }
                case 1 {
                    returndatacopy(0x00, 0x00, returndatasize())
                    return(0x00, returndatasize())
                }
        }
    }
}
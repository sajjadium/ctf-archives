import "./Gov.sol";
import "./Token.sol";

contract Deployer{

    event Deploy(address token, address gov);

    function init() external returns(address,address) {
        AAA token=new AAA();
        Gov gov=new Gov(IVotes(token));
        token.transfer(address(gov),token.balanceOf(address(this)));
        
        emit Deploy(address(token), address(gov));
    
        return (address(token),address(gov));
    }
}


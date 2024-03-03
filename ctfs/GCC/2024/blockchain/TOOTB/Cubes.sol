// SPDX-License-Identifier: MIT
pragma solidity 0.8.23;

contract CubeFactory {
    uint256 public constant CUBE_COST = 1 ether;

    struct Cube {
        uint256 centerX;
        uint256 centerY;
        uint256 centerZ;
        uint256 size;
    }

    mapping(address user => uint256 cubeBalance) public cubeBalanceOf;
    mapping(uint256 id   => Cube) public cubes;

    address owner; 

    uint256 public totalCubes;
    uint256 private treshold;

    event CubeCreated(address indexed creator, uint256 indexed cubeId);
    event Withdrawal(address indexed owner, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

  
    function createCube(uint256 _centerX, uint256 _centerY, uint256 _centerZ, uint256 _size) public payable {
        require(msg.value >= CUBE_COST, "Insufficient payment for cube creation");

        uint256 cubeId = totalCubes++;
        cubes[cubeId] = Cube(_centerX, _centerY, _centerZ, _size);
        cubeBalanceOf[msg.sender]++;
        treshold ++;

        emit CubeCreated(msg.sender, cubeId);
    }

    function getUserCubeBalance(address _user) public view returns (uint256) {
        return cubeBalanceOf[_user];
    }

    function withdraw() public {
        require(msg.sender == owner || address(this).balance >= 10_000 ether, "Not owner or Insufficient funds for withdrawal"); 

        payable(msg.sender).transfer(address(this).balance);

        emit Withdrawal(msg.sender, address(this).balance);
    }
}
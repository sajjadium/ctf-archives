// SPDX-License-Identifier: MIT
pragma solidity 0.4.24;

import './Initializable.sol';

contract TotallySecureDapp is Initializable {
    struct Post {
        string title;
        string content;
    }

    string public _contractId;
    address public _owner;
    address[] public _authors;
    Post[] public _posts;
    bool public _flagCaptured;

    event PostPublished(address indexed author, uint256 indexed index);
    event PostEdited(address indexed author, uint256 indexed index);
    event PostRemoved(address indexed author, uint256 indexed index);
    event FlagCaptured(address indexed capturer);

    modifier onlyOwner() {
        require(msg.sender == _owner, 'Caller is not the owner');
        _;
    }

    function initialize(string memory contractId) public initializer {
        _contractId = contractId;
        _owner = msg.sender;
        _flagCaptured = false;
    }

    function addPost(string title, string content) external {
        Post memory post = Post(title, content);
        _posts.push(post);
        _authors.push(msg.sender);
        emit PostPublished(msg.sender, _posts.length - 1);
    }

    function editPost(
        uint256 index,
        string title,
        string content
    ) external {
        _authors[index] = msg.sender;
        _posts[index] = Post(title, content);
        emit PostEdited(msg.sender, index);
    }

    function removePost(uint256 index) external {
        if (int256(index) < int256(_posts.length - 1)) {
            for (uint256 i = index; i < _posts.length - 1; i++) {
                _posts[i] = _posts[i + 1];
                _authors[i] = _authors[i + 1];
            }
        }
        _posts.length--;
        _authors.length--;
        emit PostRemoved(msg.sender, index);
    }

    function nPosts() public view returns (uint256) {
        return _posts.length;
    }

    function captureFlag() external onlyOwner {
        require(address(this).balance > 0.005 ether, 'Balance too low');
        _flagCaptured = true;
        emit FlagCaptured(msg.sender);
    }

    function() external payable {
        revert('Contract does not accept payments');
    }
}

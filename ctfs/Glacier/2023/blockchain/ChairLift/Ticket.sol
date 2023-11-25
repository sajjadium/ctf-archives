// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Ticket {
    bytes32 private constant DOMAIN_SEPARATOR_TYPEHASH = keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)");
    bytes32 private constant PERMIT_TYPEHASH = keccak256("Permit(address from,address to,uint256 tokenId,uint256 nonce,uint256 deadline)");

    mapping(address => uint256) public nonces;
    mapping (uint256 => address) private _owners;
    mapping (uint256 => address) private _tokenApprovals;
    mapping (address => mapping (address => bool)) private _operatorApprovals;

    string private _name;
    address owner;
    uint256 id;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed _owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed _owner, address indexed operator, bool approved);

    constructor(string memory name_) {
        _name = name_;
        owner = msg.sender;
        id = 0;
    }

    //------------------------------------------------ PUBLIC FUNCTIONS ------------------------------------------------//

    function ownerOf(uint256 tokenId) public view returns (address) {
        return _owners[tokenId];
    }

    function approve(address to, uint256 tokenId) public {
        address ticketOwner = ownerOf(tokenId);
        require(to != ticketOwner, "Ticket: approval to current owner");
        require(msg.sender == ticketOwner || isApprovedForAll(ticketOwner, msg.sender),
            "Ticket: approve caller is not owner nor approved for all"
        );
        _tokenApprovals[tokenId] = to;
        emit Approval(ticketOwner, to, tokenId);
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        require(_owners[tokenId] != address(0), "Ticket: approved query for nonexistent token");
        return _tokenApprovals[tokenId];
    }

    function setApprovalForAll(address operator, bool approved) public {
        require(operator != msg.sender, "Ticket: approve to caller");
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    function isApprovedForAll(address _owner, address operator) public view returns (bool) {
        return _operatorApprovals[_owner][operator];
    }

    function transferFrom(address from, address to, uint256 tokenId) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Ticket: transfer caller is not owner nor approved");
        _transfer(from, to, tokenId);
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Ticket: transfer caller is not owner nor approved");
        _safeTransfer(from, to, tokenId, _data);
    }

    function transferWithPermit(address from, address to, uint256 tokenId, uint256 deadline, uint8 v, bytes32 r, bytes32 s) public {
        require(block.timestamp <= deadline, "Ticket: permit expired");
        bytes32 digest = keccak256(abi.encodePacked("\x19\x01", _getDomainSeparator(), keccak256(abi.encode(PERMIT_TYPEHASH, from, to, tokenId, nonces[from]++, deadline))));
        address signer = ecrecover(digest, v, r, s);
        require(signer == from, "Ticket: invalid permit");
        _transfer(from, to, tokenId);
    }

    function mint(address target) public {
        require(msg.sender == owner, "Ticket: Only the owner can mint tickets");
        
        _owners[id] = target;

        id++;
    }

    function burn(uint256 tokenId) public {
        require(msg.sender == owner, "Ticket: caller is not owner nor approved");
        
        _owners[tokenId] = address(0);
    }

    //------------------------------------------------ INTERNAL FUNCTIONS ------------------------------------------------//

    function _transfer(address from, address to, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from, "Ticket: transfer of token that is not own");
        require(to != address(0), "Ticket: transfer to the zero address");

        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }

    function _safeTransfer(address from, address to, uint256 tokenId, bytes memory _data) internal {
        _transfer(from, to, tokenId);
        require(_checkOnERC721Received(from, to, tokenId, _data), "Ticket: transfer to non ERC721Receiver implementer");
    }

    function _checkOnERC721Received(address from, address to, uint256 tokenId, bytes memory _data) internal returns (bool) {
        if (_isContract(to)) {
            try IERC721Receiver(to).onERC721Received(msg.sender, from, tokenId, _data) returns (bytes4 retval) {
                return retval == IERC721Receiver(to).onERC721Received.selector;
            } catch (bytes memory reason) {
                if (reason.length == 0) {
                    revert("Ticket: transfer to non ERC721Receiver implementer");
                } else {
                    assembly {
                        revert(add(32, reason), mload(reason))
                    }
                }
            }
        } else {
            return true;
        }
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        require(_owners[tokenId] != address(0), "Ticket: operator query for nonexistent token");
        address _owner = ownerOf(tokenId);
        return (spender == _owner || getApproved(tokenId) == spender || isApprovedForAll(_owner, spender));
    }

    function _approve(address to, uint256 tokenId) internal {
        _tokenApprovals[tokenId] = to;
        emit Approval(ownerOf(tokenId), to, tokenId);
    }


    function _getChainId() internal view returns (uint256 chainId) {
        assembly {
            chainId := chainid()
        }
    }

    function _getDomainSeparator() private view returns (bytes32) {
        return keccak256(abi.encode(
            DOMAIN_SEPARATOR_TYPEHASH,
            keccak256(bytes(_name)),
            keccak256(bytes("1")),
            _getChainId(),
            address(this)
        ));
    }

    function _isContract(address _addr) private view returns (bool){
        uint32 size;
        assembly {
            size := extcodesize(_addr)
        }
        return (size > 0);
    }
}

interface IERC721Receiver {
    function onERC721Received(address operator, address from, uint256 tokenId, bytes calldata data) external returns (bytes4);
}

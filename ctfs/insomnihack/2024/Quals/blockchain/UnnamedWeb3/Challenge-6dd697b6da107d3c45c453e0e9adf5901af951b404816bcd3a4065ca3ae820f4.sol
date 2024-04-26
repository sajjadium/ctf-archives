// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.19;

contract DomainRegistry {
    struct DomainDetails {
        address owner;
        string ip;
    }

    mapping(string => DomainDetails) domains;
    address signer;

    event DomainRegistered(string domain, address owner, string ip);
    event DomainTransfered(string domain, address owner, string ip);
    event TransferInitiated(string domain, address destination);
    event IpUpdated(string domain, string newIp);

    constructor(address _signer) {
        signer = _signer;
    }

    function registerInsoDomain(
        string memory domain,
        string memory ip
    ) public payable {
        require(msg.value == 1 ether, "Registration fee is 1 ETH");

        domain = string.concat(domain, ".inso");
        require(
            domains[domain].owner == address(0),
            "Domain already registered"
        );

        DomainDetails memory newDomain = DomainDetails({
            owner: msg.sender,
            ip: ip
        });

        domains[domain] = newDomain;

        emit DomainRegistered(domain, msg.sender, ip);
    }

    function verify(
        string memory domain,
        address owner,
        bytes memory signature
    ) private view returns (bool) {
        domain = string(abi.encodePacked(domain, "."));

        uint8 partCount = 0;
        for (uint i = 0; i < bytes(domain).length; i++) {
            if (bytes(domain)[i] == ".") {
                partCount++;
                require(partCount <= 64, "too many dots");
            }
        }

        bytes32[] memory parts = new bytes32[](partCount);
        uint8 partIndex = 0;
        string memory part;
        for (uint i = 0; i < bytes(domain).length; i++) {
            if (bytes(domain)[i] == ".") {
                part = string(abi.encodePacked(part, partCount - partIndex));
                bytes32 tmp;
                assembly {
                    tmp := mload(add(part, 32))
                }
                parts[partIndex] = tmp;
                partIndex++;
                part = "";
            } else {
                part = string(abi.encodePacked(part, bytes(domain)[i]));
            }
        }

        for (uint i = 0; i < partCount; i++) {
            bytes32 r;
            bytes32 s;
            uint8 v = uint8(signature[i * 65 + 64]);
            assembly {
                r := mload(add(signature, add(32, mul(i, 65))))
                s := mload(add(signature, add(64, mul(i, 65))))
            }
            bytes32 hash = keccak256(abi.encodePacked(parts[i], owner));
            require(ecrecover(hash, v, r, s) == signer, "Invalid signature");
        }

        return true;
    }

    function initiateTransfer(
        string memory domain,
        address destination
    ) public {
        require(
            domains[domain].owner == msg.sender,
            "Transfer must be initiated by owner"
        );

        emit TransferInitiated(domain, destination);
    }

    function transferDomain(
        string memory domain,
        string memory ip,
        bytes memory transferCode
    ) public {
        if (!verify(domain, msg.sender, transferCode)) {
            revert("Invalid transfer code");
        }

        DomainDetails memory newDomain = DomainDetails({
            owner: msg.sender,
            ip: ip
        });

        domains[domain] = newDomain;

        emit DomainTransfered(domain, msg.sender, ip);
    }

    function getDomainOwner(
        string memory domain
    ) public view returns (address) {
        return domains[domain].owner;
    }

    function updateIp(string memory domain, string memory newIp) public {
        require(
            domains[domain].owner == msg.sender,
            "Only owner can update IP"
        );

        domains[domain].ip = newIp;

        emit IpUpdated(domain, newIp);
    }

    function resolveIp(
        string memory domain
    ) public view returns (string memory ip) {
        return domains[domain].ip;
    }

    function withdraw() public {
        require(msg.sender == signer, "Only signer can withdraw");
        payable(msg.sender).transfer(address(this).balance);
    }
}

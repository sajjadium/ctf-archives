# Modern Cryptocomputer

EOSIO (https://eos.io/) is an incredible blockchain that enables users to run smart contracts, in a way that mimics modern computers (with BIOS, RAM, CPU...) but in a distributed way.

An EOSIO node was revolutionized in order to provide a feature which was sadly missing in the main blockchain: CRC32 checksum computations!
But the people behind this revolution fear for the security of this blockchain.
So they added a secret flag to the virtual machine of the blockchain, that only privileged contracts (like "root users") can read.
Will you be able to steal this flag?

In order to make things more accessible for newcomers, an "easy to find" flag was also inserted in a smart contract.

# Details

* The modified node is available at `modern-cryptocomputer.donjon-ctf.io:30510`.
* This node is running in a container which configuration is provided.
* The tools from the official EOSIO blockchain can be used to interact with the modified node.
* In order to deploy a smart contract, 2048 accounts were created. The access to these accounts is protected with the development keys documented in EOSIO's official website.
* The second flag should only be available after the first flag has been found.
* To improve the stability of the challenge, the node is restarted every hour from a clean known-good state.
* The challenge does not consist in cracking the private key of the modified node.

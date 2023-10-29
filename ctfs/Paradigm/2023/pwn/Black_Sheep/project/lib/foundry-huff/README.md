<img align="right" width="400" height="160" top="140" src="./assets/foundry_huff_banner.jpg">


# Foundry x Huff

[![ci](https://github.com/huff-language/huff-rs/actions/workflows/ci.yaml/badge.svg)](https://github.com/huff-language/huff-rs/actions/workflows/ci.yaml) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Discord](https://img.shields.io/discord/980519274600882306)

A [foundry](https://github.com/foundry-rs/foundry) library for working with [huff](https://github.com/huff-language/huff-rs) contracts. Take a look at our [project template](https://github.com/huff-language/huff-project-template) to see an example project that uses this library.


## Installing

First, install the [huff compiler](https://github.com/huff-language/huff-rs) by running:
```
curl -L get.huff.sh | bash
```

Then, install this library with [forge](https://github.com/foundry-rs/foundry):
```
forge install huff-language/foundry-huff
```


## Usage

The HuffDeployer is a Solidity library that takes a filename and deploys the corresponding Huff contract, returning the address that the bytecode was deployed to. To use it, simply import it into your file by doing:

```js
import {HuffDeployer} from "foundry-huff/HuffDeployer.sol";
```

To compile contracts, you can use `HuffDeployer.deploy(string fileName)`, which takes in a single string representing the filename's path relative to the `src` directory. Note that the file ending, i.e. `.huff`, must be omitted.
Here is an example deployment (where the contract is located in [`src/test/contracts/Number.huff`](./src/test/contracts/Number.huff)):

```solidity
// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import {HuffDeployer} from "foundry-huff/HuffDeployer";

interface Number {
  function setNumber(uint256) external;
  function getNumber() external returns (uint256);
}

contract HuffDeployerExample {
  function deploy() public {
    // Deploy a new instance of src/test/contracts/Number.huff
    address addr = HuffDeployer.deploy("test/contracts/Number");

    // To call a function on the deployed contract, create an interface and wrap the address like so
    Number number = Number(addr);
  }
}
```

To deploy a Huff contract with constructor arguments, you can _chain_ commands onto the HuffDeployer.

For example, to deploy the contract [`src/test/contracts/Constructor.huff`](src/test/contracts/Constructor.huff) with arguments `(uint256(0x420), uint256(0x420))`, you are encouraged to follow the logic defined in the `deploy` function of the `HuffDeployerArguments` contract below.

```solidity
// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import {HuffDeployer} from "foundry-huff/HuffDeployer";

interface Constructor {
  function getArgOne() external returns (address);
  function getArgTwo() external returns (uint256);
}

contract HuffDeployerArguments {
  function deploy() public {
    // Deploy the contract with arguments
    address addr = HuffDeployer
      .config()
      .with_args(bytes.concat(abi.encode(uint256(0x420)), abi.encode(uint256(0x420))))
      .deploy("test/contracts/Constructor");

    // To call a function on the deployed contract, create an interface and wrap the address
    Constructor construct = Constructor(addr);

    // Validate we deployed the Constructor with the correct arguments
    assert(construct.getArgOne() == address(0x420));
    assert(construct.getArgTwo() == uint256(0x420));
  }

  function depreciated_deploy() public {
    address addr = HuffDeployer.deploy_with_args(
      "test/contracts/Constructor",
      bytes.concat(abi.encode(uint256(0x420)), abi.encode(uint256(0x420)))
    );

    // ...
  }
}
```

HuffDeployer also enables you to instantiate contracts, from the test file, even if they have _no constructor macro_!

This is possible by using [Foundry](https://github.com/foundry-rs/foundry)'s [ffi](https://book.getfoundry.sh/cheatcodes/ffi.html) cheatcode.

_NOTE: It is highly recommended that you read the foundry book, or at least familiarize yourself with foundry, before using this library to avoid easily susceptible footguns._

Let's use the huff contract [`src/test/contracts/NoConstructor.huff`](./src/test/contracts/NoConstructor.huff), which has no defined constructor macro. The inline-instantiation defined in the `deploy` function of the `HuffDeployerCode` contract below is recommended.

```solidity
// SPDX-License-Identifier: Apache-2.0
pragma solidity >=0.7.0 <0.9.0;

import {HuffDeployer} from "foundry-huff/HuffDeployer";

interface Constructor {
  function getArgOne() external returns (address);
  function getArgTwo() external returns (uint256);
}

contract HuffDeployerCode {

  function deploy() public {
    // Define a new constructor macro as a string
    string memory constructor_macro = "#define macro CONSTRUCTOR() = takes(0) returns (0) {"
      "    // Copy the first argument into memory \n"
      "    0x20                        // [size] - byte size to copy \n"
      "    0x40 codesize sub           // [offset, size] - offset in the code to copy from\n "
      "    0x00                        // [mem, offset, size] - offset in memory to copy to \n"
      "    codecopy                    // [] \n"
      "    // Store the first argument in storage\n"
      "    0x00 mload                  // [arg] \n"
      "    [CONSTRUCTOR_ARG_ONE]       // [CONSTRUCTOR_ARG_ONE, arg] \n"
      "    sstore                      // [] \n"
      "    // Copy the second argument into memory \n"
      "    0x20                        // [size] - byte size to copy \n"
      "    0x20 codesize sub           // [offset, size] - offset in the code to copy from \n"
      "    0x00                        // [mem, offset, size] - offset in memory to copy to \n"
      "    codecopy                    // [] \n"
      "    // Store the second argument in storage \n"
      "    0x00 mload                  // [arg] \n"
      "    [CONSTRUCTOR_ARG_TWO]       // [CONSTRUCTOR_ARG_TWO, arg] \n"
      "    sstore                      // [] \n"
      "}";

    // Deploy the contract with arguments
    address addr = HuffDeployer
      .config()
      .with_args(bytes.concat(abi.encode(uint256(0x420)), abi.encode(uint256(0x420))))
      .with_code(constructor_macro)
      .deploy("test/contracts/NoConstructor");

    // To call a function on the deployed contract, create an interface and wrap the address
    Constructor construct = Constructor(addr);

    // Validate we deployed the Constructor with the correct arguments
    assert(construct.getArgOne() == address(0x420));
    assert(construct.getArgTwo() == uint256(0x420));
  }

  function depreciated_deploy_with_code() public {
    address addr = HuffDeployer.deploy_with_code(
      "test/contracts/Constructor",
      constructor_macro
    );

    // ...
  }
}
```

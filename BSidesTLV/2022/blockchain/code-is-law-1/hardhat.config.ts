import { HardhatUserConfig } from "hardhat/config";
import "@nomiclabs/hardhat-etherscan";
import "@nomiclabs/hardhat-waffle";
import "@typechain/hardhat";
import "hardhat-ctf";
import { ethers } from "ethers";
import { EthereumProvider, JsonRpcRequest } from "hardhat/types";
import { JsonRpcResponse, SuccessfulJsonRpcResponse } from "hardhat/internal/util/jsonrpc";

const config: HardhatUserConfig = {
  solidity: "0.8.4",
  ctfRemoteNode: "wss://code-is-law-1-mp6m2lcoiq-ey.a.run.app",
};

export default config;

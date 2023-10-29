# Deployment addresses

The latest version of `@uniswap/v3-core`, `@uniswap/v3-periphery` are deployed to Ethereum mainnet and all testnets
at the same addresses.

The source code is verified with Etherscan on all networks, for all contracts except `UniswapV3Pool`.
We are working on getting the `UniswapV3Pool` contract verified with Etherscan.

These addresses are final and were deployed from these npm package versions:

- `@uniswap/v3-core`: [`1.0.0`](https://github.com/Uniswap/uniswap-v3-core/tree/v1.0.0)
- `@uniswap/v3-periphery`: [`1.0.0`](https://github.com/Uniswap/uniswap-v3-periphery/tree/v1.0.0)

| Contract                           | Address                                      | Source Code                                                                                                                   |
| ---------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| UniswapV3Factory                   | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | https://github.com/Uniswap/uniswap-v3-core/blob/v1.0.0/contracts/UniswapV3Factory.sol                                         |
| Multicall2                         | `0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696` | https://etherscan.io/address/0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696#code                                                  |
| ProxyAdmin                         | `0xB753548F6E010e7e680BA186F9Ca1BdAB2E90cf2` | https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.4.1-solc-0.7-2/contracts/proxy/ProxyAdmin.sol                  |
| TickLens                           | `0xbfd8137f7d1516D3ea5cA83523914859ec47F573` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/lens/TickLens.sol                                       |
| Quoter                             | `0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/lens/Quoter.sol                                         |
| SwapRouter                         | `0xE592427A0AEce92De3Edee1F18E0157C05861564` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/SwapRouter.sol                                          |
| NFTDescriptor                      | `0x42B24A95702b9986e82d421cC3568932790A48Ec` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/libraries/NFTDescriptor.sol                             |
| NonfungibleTokenPositionDescriptor | `0x91ae842A5Ffd8d12023116943e72A606179294f3` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/NonfungibleTokenPositionDescriptor.sol                  |
| TransparentUpgradeableProxy        | `0xEe6A57eC80ea46401049E92587E52f5Ec1c24785` | https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.4.1-solc-0.7-2/contracts/proxy/TransparentUpgradeableProxy.sol |
| NonfungiblePositionManager         | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/NonfungiblePositionManager.sol                          |
| V3Migrator                         | `0xA5644E29708357803b5A882D272c41cC0dF92B34` | https://github.com/Uniswap/uniswap-v3-periphery/blob/v1.0.0/contracts/V3Migrator.sol                                          |

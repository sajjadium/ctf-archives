It's rumored that you can get a free flag on the Solana blockchain, but it's locked behind a secret! Can you still obtain it?

The contract is deployed at: Secret1111111111111111111111111111111111111

This challenge has the same setup as all Solana Smart Contract challenges: a validator running in a docker container that you have to interact with via RPC.

This challenge can be solved by just using the store-cli and solana cli.

If you got the secret, you can get the flag by calling

store-cli -k ./keys/rich-boi.json get-flag <flag_depot_address> <secret>

We recommend using the Solana PoC Framework which facilitates fast exploit development. Alternatively you can also use the official rust api, the official js api or any other way you can think of interacting with the RPC server. Solana also has a multitude of cli tools. Please note however that due to setup limitations, the TPU port of the validator is not exposed, which means the solana program deploy command will not work. The Solana PoC Framework has a function for this that only uses the rpc endpoint and will work.

The solana explorer works with any cluster your browser can reach. Just click on the Mainnet Beta button and enter the url of the RPC endpoint into the Custom text field. Checking the Enable custom url param checkbox might also be useful for collaboration. The explorer allows you to inspect accounts and transactions and has a bunch of useful features.

The goal of these challenges is to obtain a flag-token (mint F1agMint11111111111111111111111111111111111). After you got one, you have to call the flag contract F1ag111111111111111111111111111111111111111. The instruction data is ignored, the first account has to be a spl-token account that contains a flag token and the second account has to be the owner of the token account. The second account needs to sign the transaction, to proof that you really got the flag.

A good starting point is the Solana documentation:

    https://docs.solana.com/developing/programming-model/overview
    https://spl.solana.com/token#operational-overview
    https://docs.solana.com/developing/clients/jsonrpc-api

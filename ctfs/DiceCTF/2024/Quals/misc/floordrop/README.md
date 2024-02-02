hpmv, orion

Ever heard of airdrops? Well, we're doing a floordrop. We're dropping the flag on the floor. Go pick it up.

This challenge happens on DiceChain, an Ethereum-compatible network started using go-ethereum with the genesis.json provided to you. You may start a challenge attempt at any time by connecting to the provided nc.

During each challenge attempt,

    The server will generate a challenge for you to solve and send a transaction that calls setChallenge(the challenge) on the ProofOfWork contract.
    Two seconds later, the server will send another transaction that calls expireChallenge() on the same contract.
    Your goal is to solve the challenge and submit the solution by calling solveChallenge(the solution encoded in bigendian bytes, random nonce), before the challenge expires. A script to solve the challenge has been provided to you in solve.py.
    If you submit the correct solution before the challenge expires, a flag will be printed in the same nc session.

You're encouraged to use the mock challenge (menu option 1) to familiarize yourself with the challenge setup. Also, to help with your understanding, an example series of transactions that would yield a successful solve can be found in block 154.

Links:

    Block explorer: https://floordrop.hpmv.dev/
    RPC: https://floordrop-rpc.hpmv.dev/
    Faucet: floordrop-faucet.mc.ax (use to get some free DICE!).

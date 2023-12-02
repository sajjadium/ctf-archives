All Tony's shitcoins got hacked. Liquidity providers of those shitcoins sued Tony. To reimburse the liquidity providers, Tony built a GameFi about ducks (ducks are the cutest animal!)


Running the challenge locally:

Assuming you have Foundry and Node.js installed, you can run the challenge locally with the following commands:
```
# start an anvil instance
anvil &

# use the default private key (the challenge does not use this key)
export PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# deploy the challenge
cd project && forge create Challenge --private-key $PRIVATE_KEY && cd ..

# start the agents
cd agents
npm install
DUCK_ADDRESS={the deployed contract address} node index.js    
```

Then, the chain shall be up at `http://localhost:8545` and the web interface at `http://localhost:3000`.

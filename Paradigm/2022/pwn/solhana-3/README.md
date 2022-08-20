# hana solana ctf

ok like all the best software engineers i got the technicals done on time and under budget but left documentation for future me. its now the future and i am pissed

in lieu of getting fancy with it i will just run you through the basics

## my friends at paradigm

the dockerfile should be ready to go. to run the server. `git checkout master` and from the `hana/` directory run whatever docker commands you need based on your setup. for me this works: `docker build -t solhana . ; docker run -d -P solhana` and proxy the port however you intend to

to generate stuff to give to players `git checkout hana-player`, change line 9 of `client/api.js` to where youre hosting this (or tell me where), and run `./make_tarball` and give them `solhana-ctf.tar.gz`. please do not give them a tarball from master it will spoil all of my precious secrets

## my friends not at paradigm and also my enemies

all challenges are in anchor. (id love to do some vanilla solana next year tho.) i wrote against anchor 0.24.2 and solana 1.9. using a newer solana version is probably fine, using a newer anchor probably not, because of the tendency of the latter to introduce breaking changes

im gonna go through what all the directories are, explain how to set up locally, explain how to actually do the ctf part, and then intro the challenges

### dir rundown

* `elf/`: prebuilt bpf binaries of the three challenges so you dont have to build them. these should work as-is
* `idl/`: idls for the challenges
* `chain/`: code of the challenges for your perusal and edification. note that any function gated by `MASTER` (commented out in your version is *not in play*. theres a secret key to prevent you from doing funny business, you should not be able to call these on the server at all
* `client/`: skeleton for your attack code. you should be able to add whatever imports you need , code entirely within tha `attack()` function, and run it to check your win status and get the flag
* `server/`: the proxy server that sits between you and a test validator. please admire it, 90% of my time was writing this thing, not the challenges. but the important thing here is in `src/challenge.rs` you can see the setup code for the challenges, with comments explaining what the stuff is

### how to run local

ok so you cant run the server lol. but thats ok, you dont need it! start yourself up a `solana-test-validator`, then in `server/` run `cargo run --bin setup_chain`. this will deploy the challenge programs on your local validator, run all the necessary account setup code, and write out a file `player.json` in the parent dir

`player.json` is your best friend. it provides *every* account pubkey you should need, except for your own associated token accounts or accounts you may decide to create yourself. *you do not need to generate addresses or bumps from seeds*

`player.json` contains the keypair you use as a player, the endpoint to contact your local validator _or_ the server, and the accounts for each challenge. if you look at any of `client/challenge{1,2,3}.js` you will notice i also load the idls and the player file for you. i create a series of variables like `player` (your keypair) and most interestingly `conn`, a standard solana `Connection` object

the server for the actual ctf submissions and win verification is, among other things, a proxy that implements a small subset of solana jsonrpc. this means that as long as you use the `conn` object or the helpers in `api.js`, and as long as you dont use `confirmTransaction` or its variants, or `getAccount` or anything like that, *code you write against your local validator will work almost as-is against the ctf server*. this includes multiple transactions; the ctf server is fully stateful

the one exception is if you should just so happen to decide you need to deploy your *own* program to complete a challenge (this is a hint). in that case use `anchor deploy` for your local validator, but use the api helper for the ctf server, invoked `api.deployProgram(baseUrl, player.publicKey, fs.readFileSync("path/to/program.so"));`

set up your `client/` dir by running `yarn` and then you should be able to code in the challenge files. the `api.getFlag` call will fail but you can inspect the chain directly, a luxury you lack in ctf world

### how to run international

from `client/` run `node create-player.js` and a new `player.json` file will be delivered to you from on cloud, and the corresponding accounts will be set up on the server. this has the same format as the one generated locally and serves as a drop-in replacement as long as you used its values instead of hardcoding anything

if your challenge is good to go, run the challenge file, and hopefully get back a string from the server to plug into the leaderboard site or whatever (i dont know how this part is being done)

please be nice to our poor server and treat it as a success validator and not a dev platform. it is much easier to work against a local validator where you can inspect accounts. the server only supports these rpc calls, by design:
* `sendTransaction`
* `getLatestBlockhash`
* `getMinimumBalanceForRentExemption`

do *not* share the public key of the keypair you get from `player.json`, *it is effectively a credential*. i didnt want to implement fucking message signing or whatever shit. if you share your pubkey people can steal your precious flags. pls dont

### challenge one

theres a brand new ponzi scheme in town that lets people deposit and withdraw their bitcoin. why would they want to do this? no one knows

but what they *do* know is satoshi nakamoto himself has deposited one entire bitcoin into this secure protocol audited by [i dont think im allowed to make this joke]

steal it

### challenge two

theres a brand new ponzi scheme in town that lets people deposit and withdraw their ethereum. why would they want to do this? no one knows

in fact, they can deposit three kinds of ethereum: wormhole-wrapped eth, sollet-wrapped eth, and lido staked eth (i wrote this challenge back in may when it still held peg ok). the protocol also functions as a stableswap between these three variants

each of the three pool has 100k units of its eth variant. steal at least half the total

### challenge three

theres a brand new ponzi scheme in town that lets people deposit and withdraw their atomcoin. why would they want to do this? please stop asking me this

what is atomcoin? its an indivisible spl token because trust me you dont want to deal with decimals on this one

this protocol designed by some fucking idiot allows you to flash loans, borrowing a sum of tokens in one instruction, and repaying it with a separate instruction in the same transaction. i will be nice and say you do *not* need to use `deposit` or `withdraw` here, *only* `borrow` and `repay`

the pool has 100 atomcoin in it. steal at least 98

### thats it

i hope you enjoy the challenges and dont get mad at me if the infrastructure breaks or some of them are too hard. this is my first ctf attempt

ive done my best to be player friendly. but maybe i failed. at least im friendly on twitter

as they say, theres always next year!

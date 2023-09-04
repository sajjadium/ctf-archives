Solana
Going once, going twice!
Every man here has a price!


# Setup

!! siced from idekctf2023/babysolana chals !!
!! too lazy to setup anchor myself so thx <3 !!

Use `framework/` to locally setup the challenge
Use `framework-solve/` to solve the challenge locally and remotely

Edit `framework-solve/solve/programs/solve/src/lib.rs` with your exploit


## Deployment
- Run `docker build -t solana-challenge-2 .` in the `framework` directory
- Run `docker run -d -p 1337:1337 solana-challenge-2`


## Building the solution
- Run `build_solution.sh` in the `solution` directory
- Run `target/release/solve-framework`

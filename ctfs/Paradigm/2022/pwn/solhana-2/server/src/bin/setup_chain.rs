use std::fs;
use serde_json;

use server::*;

// this is a binary to do the chain setup that the server normally does
// and also to create a single player, normally behind an endpoint
// this allows a player to test challenges locally without axum or sqlite
// solutions written against a local chain ought to work against our solution validator as-is
// the axum interface is designed as a drop-in replacement for the relevant subset of solana jsonrpc

// XXX TODO FIXME challenges are NOT runnable as-is
// challenge setup functions are gated by a SECURITY-CRITICAL master key
// we need to comment this out on the contracts delivered to them

const PLAYER_FILE: &str = "local_player.json";

#[tokio::main]
async fn main() {
    println!("running chain setup for player use");

    let rpc = rpc();
    if let Err(_) = rpc.get_health().await {
        println!("could not connect to chain; are you running on {}?", rpc.url());
        return;
    }

    // this is to make it idempotent but tbh you should run the test validator with --reset
    let _ = challenge::setup(&rpc).await;

    let accounts = make_new_player(&rpc, &rpc.url()).await.unwrap();

    fs::write(PLAYER_FILE, serde_json::to_string(&accounts).unwrap()).unwrap();
    println!("wrote player data to {}", PLAYER_FILE);

    return;
}

use std::str::FromStr;
use axum::{
    routing::get, routing::post, extract::Path,
    Router, body::Bytes, Json,
};
use serde::{ Serialize, Deserialize };
use serde_json::{ json, Value, value::from_value };
use hyper::http::StatusCode;
use sqlite as sql;

use solana_sdk::{
    pubkey::Pubkey, signer::keypair::Keypair, signature::{ Signer, Signature },
    commitment_config::CommitmentConfig,
};
use solana_client::{
    rpc_request::RpcRequest, rpc_config::RpcSendTransactionConfig,
};
use solana_transaction_status::UiTransactionEncoding;

use server::*;

// im gonna use fresh db/http connections liek a retard for now
// but axum has a thing they call "handlers" for connection pools
// note sqlite::open defaults to rw
// i think it also defaults to serialized
// i can use set_no_mutex connections as long as threads dont share them

// i think i actually dont need a connection pool for sqlite lol
// its just a file, theres no such thing as a "connection"
// this also explains why the library exposes no close method

const SRV_URL: &str = "http://127.0.0.1:3000";
const DB_PATH: &str = "hana-ctf.db";

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RpcEnvelopeReq {
    pub jsonrpc: String,
    pub id: String,
    pub method: String,
    pub params: Vec<Value>,
}

// RANDOM SHIT UP HERE

fn code<T>(code: u16, msg: &str) -> Result<T, (StatusCode, String)> {
    let msg = if msg == "" { "this shouldnt happen" } else { msg };
    Err((StatusCode::from_u16(code).unwrap(), msg.to_string()))
}

fn db_rw() -> Result<sql::Connection, sqlite::Error> {
    let flags = sql::OpenFlags::new()
        .set_read_write()
        .set_full_mutex();

    let db = sql::Connection::open_with_flags(DB_PATH, flags)?;
    db.execute("pragma foreign_keys = on")?;

    Ok(db)
}

fn db_ro() -> Result<sql::Connection, sqlite::Error> {
    let flags = sql::OpenFlags::new()
        .set_read_only()
        .set_full_mutex();

    sql::Connection::open_with_flags(DB_PATH, flags)
}

fn check_player(db: &sql::Connection, pubkey: &str) -> Result<(i64, String), (StatusCode, String)> {
    let mut stmt = db.prepare("select id, last_signature from players where pubkey = ?").or(code(500, ""))?;
    stmt.bind(1, &*pubkey).or(code(400, "invalid pubkey for check_player"))?;

    stmt.next()
        .or(code(400, "could not find player for check_player"))
        .and_then(|row|
            if row == sql::State::Row {
                let id = stmt.read::<i64>(0).or(code(500, ""))?;
                let sig = stmt.read::<String>(1).or(code(500, ""))?;
                Ok((id, sig))
            }
            else {
                code(400, "could not find player for check_player")
            })
}

// ROUTES DOWN HERE

// generate a new keypair, return it and all challenge accounts addresses
// the pubkey is an auth credential, so we dont let people bring their own
async fn create_player() -> Result<Json<challenge::Accounts>, (StatusCode, String)> {
    let rpc = rpc();
    let db = db_rw().or(code(500, "failed to connect to db"))?;

    let accounts = make_new_player(&rpc, SRV_URL).await.or(code(500, "failed to create player"))?;
    let keypair = Keypair::from_bytes(&accounts.player).or(code(500, ""))?;

    let mut stmt = db.prepare("insert into players (pubkey) values (?)").or(code(500, ""))?;
    stmt.bind(1, &*keypair.pubkey().to_string()).or(code(500, ""))?;
    stmt.next().or(code(500, "failed to insert player"))?;

    Ok(Json(accounts))
}

// this passes the listed rpc method through to solana, mostly unchanged
// the point of doing it this ugly way is so our server can be a valid connection object
// this means it should work with any solana or anchor helpers that only use these methods
async fn handle_rpc(
    Path(pubkey): Path<String>,
    Json(req): Json<RpcEnvelopeReq>,
) -> Result<Json<Value>, (StatusCode, String)> {
    let rpc = rpc();
    let db = db_rw().or(code(500, "failed to connect to db"))?;
    check_player(&db, &pubkey)?;

    // annoyingly i cant use serde_with because they dont impl FromStr
    match &*req.method {
        "sendTransaction" => {
            let config = RpcSendTransactionConfig {
                skip_preflight: true,
                encoding: Some(UiTransactionEncoding::Base64),
                ..RpcSendTransactionConfig::default()
            };

            let sig = rpc.send::<String>(
                RpcRequest::SendTransaction,
                json!([from_value::<String>(req.params[0].clone()).or(code(400, "could not parse rpc request"))?, config]),
            ).await.or(code(400, "rpc send_transaction failed"))?;

            // we retain the last sig so in check_win we can await confirmation
            // i was gonna provide a confirm endpoint but its too complicated to be worth the effort
            // web3.js confirmTransaction will never work anyway because it depends on the websocket endpoint
            let mut stmt = db.prepare("update players set last_signature = ? where pubkey = ?").or(code(500, ""))?;
            stmt.bind(1, &*sig.to_string()).or(code(500, ""))?;
            stmt.bind(2, &*pubkey.to_string()).or(code(500, ""))?;
            stmt.next().or(code(500, "failed to update player record"))?;

            Ok(Json(json!({"jsonrpc": req.jsonrpc, "id": req.id, "result": sig.to_string()})))
        },
        "getLatestBlockhash" => {
            let blockhash = rpc.get_latest_blockhash_with_commitment(
                CommitmentConfig::finalized()
            ).await.or(code(500, "could not get blockhash"))?;

            // i hate my life
            Ok(Json(json!({"jsonrpc": req.jsonrpc, "id": req.id, "result": {"context": {"slot": 0}, "value": {"blockhash": blockhash.0.to_string(), "lastValidBlockHeight": blockhash.1}}})))
        },
        "getMinimumBalanceForRentExemption" => {
            let size = from_value::<usize>(req.params[0].clone()).or(code(400, "could not parse rent size arg"))?;
            let rent = rpc.get_minimum_balance_for_rent_exemption(size).await.or(code(500, "rent check failed"))?;

            Ok(Json(json!({"jsonrpc": req.jsonrpc, "id": req.id, "result": rent})))
        },
        _ => code(400, "invalid or unsupported rpc method"),
    }
}

// player submits an elf in binary in the post body, we deploy it
// programs are deployed to arbitrary addresses, which we furnish to the player
// this means anchor cpi wrappers wont work for calling into them, but nothing should require that anyway
async fn post_program(Path(pubkey): Path<String>, body: Bytes) -> Result<String, (StatusCode, String)> {
    let rpc = rpc();
    let db = db_rw().or(code(500, "failed to connect to db"))?;
    let (player_id, _) = check_player(&db, &pubkey)?;

    // make a new payer so we dont need player signatures
    let payer = Keypair::new();
    airdrop(&rpc, &payer.pubkey(), 100).await.or(code(500, "failed to airdrop"))?;

    // this is the address the program will deploy to
    let program = Keypair::new();
    let program_id = program.pubkey().to_string();

    // and now the big boy
    // note if we ever have any "the entire webserver freezes randomly" problems
    // its probably because of something accidentally sync in here lol
    // someone told me this is a common problem with tokio idk if its true
    deploy_program(&rpc, &payer, &program, body.as_ref()).await.or(code(400, "could not deploy program"))?;

    // this is more for housekeeping but maybe itll come in handy
    let mut stmt = db.prepare("insert into player_programs (player_id, pubkey) values (?, ?)").or(code(500, ""))?;
    stmt.bind(1, player_id).or(code(500, ""))?;
    stmt.bind(2, &*program_id).or(code(500, ""))?;
    stmt.next().or(code(500, "failed to insert program record"))?;

    Ok(program_id)
}

// check a given problem for a winstate and return the flag
async fn get_flag(Path((challenge, pubkey)): Path<(u32, String)>) -> Result<String, (StatusCode, String)> {
    let rpc = rpc();
    let db = db_ro().or(code(500, "failed to connect to db"))?;
    let (_, sig_str) = check_player(&db, &pubkey)?;

    // confirm the most recent transaction to avoid false negatives
    // we don't care if it succeeded, only that it isn't pending
    if sig_str != ""  {
        let sig = Signature::from_str(&sig_str).or(code(500, ""))?;
        let _ = rpc.poll_for_signature(&sig).await;
    }

    let player = Pubkey::from_str(&pubkey).or(code(400, "could not parse provided pubkey"))?;
    if let Ok(true) = challenge::check_win(&rpc, &player, challenge).await {
        let mut stmt = db.prepare("select flag from flags where challenge = ?").or(code(500, ""))?;
        stmt.bind(1, challenge as i64).or(code(400, "challenge must be an integer"))?;

        if let Ok(sql::State::Row) = stmt.next() {
            return stmt.read::<String>(0).or(code(400, "could not find challenge number"))
        };
    };

    code(400, "no win")
}

#[tokio::main]
async fn main() {
    println!("solana ctf server starting");

    // let the rpc connection scope out
    {
        let rpc = rpc();
        if let Err(_) = rpc.get_health().await {
            println!("could not connect to chain; are you running on {}?", rpc.url());
            return;
        }

        // setup is just program deployment
        // if it fails it just means its already done
        // if we want to reploy, reset the chain
        let _ = challenge::setup(&rpc).await;
    }

    println!("chain init done, opening routes");

    let app = Router::new()
        .route("/:pubkey", post(handle_rpc))
        .route("/player", post(create_player))
        .route("/program/:pubkey", post(post_program))
        .route("/flag/:challenge/:pubkey", get(get_flag));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

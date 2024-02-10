#[macro_use] extern crate rocket;

use base64::prelude::BASE64_STANDARD;
use base64::Engine as _;
use crypto::common::{read_flag, read_key};
use crypto::crypto::{sign, verify};
use curve25519_dalek_ng::ristretto::CompressedRistretto;
use curve25519_dalek_ng::scalar::Scalar;
use hex::ToHex;
use rocket::response::status::BadRequest;
use rocket::State;
use rocket::fs::NamedFile;
use serde::{Deserialize, Serialize};
use std::env;
use std::path::Path;

struct ServerState {
    secret_key: Scalar,
    min_value: u128,
    flag: String
}

#[derive(Serialize, Deserialize)]
struct Wallet {
    commitment: String,
    blinding: String,
    balance: u128
}

#[get("/<_>/checkout?<wallet>")]
fn checkout<'a>(state: &'a State<ServerState>, wallet: &'a str) -> Result<&'a str, BadRequest<&'a str>> {
    let json_wallet = BASE64_STANDARD.decode(wallet.as_bytes()).map_err(|_| BadRequest("Invalid wallet"))?;

    let wallet: Wallet = serde_json::from_str(String::from_utf8(json_wallet).map_err(|_| BadRequest("Invalid wallet"))?.as_str()).map_err(|_| BadRequest("Invalid wallet"))?;

    let commitment = match hex::decode(wallet.commitment) {
        Ok(bytes) if bytes.len() == 32 => CompressedRistretto::from_slice(bytes.as_slice()),
        _ => return Err(BadRequest("Invalid commitment"))
    };

    if wallet.balance < state.min_value {
        return Err(BadRequest("Not enough money"));
    }

    let balance = Scalar::from(wallet.balance);

    let blinding = match hex::decode(wallet.blinding) {
        Ok(bytes) if bytes.len() == 32 => Scalar::from_bytes_mod_order(bytes.try_into().unwrap()),
        _ => return Err(BadRequest("Invalid blinding"))
    };

    if verify(commitment, state.secret_key, balance, blinding) {
        Ok(state.flag.as_str())
    } else {
        Err(BadRequest("Invalid commitment"))
    }
}

#[get("/<_>")]
async fn index() -> Option<NamedFile> {
    return NamedFile::open("static/index.html").await.ok();
}

#[get("/<_>/issue")]
fn get_wallet(state: &State<ServerState>) -> String {
    let balance = Scalar::from(100u32);
    let (commitment, blinding) = sign(state.secret_key, balance);

    let wallet = Wallet {
        commitment: commitment.as_bytes().encode_hex::<String>(),
        blinding: blinding.as_bytes().encode_hex::<String>(),
        balance: 100
    };

    return BASE64_STANDARD.encode(serde_json::to_string(&wallet).unwrap().as_bytes());
}

#[launch]
fn rocket() -> _ {
    let secret_path_str = env::var("SECRET_PATH").unwrap_or(".".to_string());
    let secret_path = Path::new(&secret_path_str);
    let secret_key = read_key(&secret_path.join("secret.txt"));
    let flag = read_flag(&secret_path.join("flag.txt"));
    let min_value = 1337u128;

    let state = ServerState {
        secret_key, min_value, flag
    };

    rocket::build().manage(state).mount("/", routes![index, checkout, get_wallet])
}

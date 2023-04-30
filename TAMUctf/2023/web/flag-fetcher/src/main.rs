#![allow(clippy::type_complexity)]

use actix_files as fs;
use actix_web::http::StatusCode;
use actix_web::web::Data;
use actix_web::{get, App, Error, HttpRequest, HttpResponse, HttpServer, Responder};
use clru::CLruCache;
use cookie::Cookie;
use hex::ToHex;
use rand::{thread_rng, RngCore};
use ring::signature::{self, Ed25519KeyPair, KeyPair};
use std::num::NonZeroUsize;
use std::path::{Component, PathBuf};
use std::str::FromStr;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use tokio::sync::Mutex;

#[get("/req")]
async fn challenge(
    req: HttpRequest,
    challenges: Data<Arc<Mutex<CLruCache<usize, Vec<u8>>>>>,
) -> Result<HttpResponse, Error> {
    if let Some(id) = req.cookie("whoami") {
        if let Ok(id) = usize::from_str(id.value()) {
            let mut lock = challenges.get_ref().lock().await;
            let challenge = lock.put_or_modify(
                id,
                |_, _| {
                    let mut rng = thread_rng();
                    let mut challenge = vec![0u8; 64];
                    rng.fill_bytes(&mut challenge);
                    challenge
                },
                |_, _, _| {},
                (),
            );
            return Ok(hex::encode(challenge)
                .respond_to(&req)
                .map_into_boxed_body());
        }
    }

    Ok(HttpResponse::new(StatusCode::UNAUTHORIZED))
}

// TODO don't throw around the key so willy-nilly; we should probably only pass the public key here
#[get("/flag")]
async fn get_flag(
    req: HttpRequest,
    flag: Data<String>,
    key: Data<Arc<Ed25519KeyPair>>,
    challenges: Data<Arc<Mutex<CLruCache<usize, Vec<u8>>>>>,
) -> Result<HttpResponse, Error> {
    if let Some(id) = req.cookie("whoami") {
        if let Ok(id) = usize::from_str(id.value()) {
            let mut lock = challenges.get_ref().lock().await;
            if let Some(current) = lock.get(&id) {
                let qs = req.query_string();
                return if let Ok(sig) = hex::decode(qs) {
                    let pubkey = key.public_key().as_ref();
                    let pubkey = signature::UnparsedPublicKey::new(&signature::ED25519, pubkey);
                    if pubkey.verify(current.as_slice(), sig.as_slice()).is_ok() {
                        Ok(flag
                            .get_ref()
                            .clone()
                            .respond_to(&req)
                            .map_into_boxed_body())
                    } else {
                        Ok(HttpResponse::new(StatusCode::UNAUTHORIZED))
                    }
                } else {
                    Ok(HttpResponse::new(StatusCode::BAD_REQUEST))
                };
            }
        }
    }

    Ok(HttpResponse::new(StatusCode::UNAUTHORIZED))
}

#[get("/sign")]
async fn sign(req: HttpRequest, key: Data<Arc<Ed25519KeyPair>>) -> Result<HttpResponse, Error> {
    let qs = req.query_string();
    if let Ok(data) = hex::decode(qs) {
        let sig = key.sign(&data);
        Ok(sig
            .encode_hex::<String>()
            .respond_to(&req)
            .map_into_boxed_body())
    } else {
        Ok(HttpResponse::new(StatusCode::BAD_REQUEST))
    }
}

#[get("/static/{filename:.*}")]
async fn static_files(req: HttpRequest) -> Result<fs::NamedFile, Error> {
    let requested: PathBuf = req.match_info().query("filename").parse()?;
    // deny path traversal
    let requested: PathBuf = requested
        .components()
        .filter(|&entry| entry != Component::ParentDir)
        .collect();

    let mut path = PathBuf::from_str("static").unwrap();
    path.extend(&requested);

    let file = fs::NamedFile::open(path)?;
    Ok(file.use_last_modified(true))
}

#[get("/")]
async fn index(req: HttpRequest, visitor: Data<AtomicUsize>) -> Result<HttpResponse, Error> {
    let mut res = fs::NamedFile::open("index.html")?
        .use_last_modified(true)
        .into_response(&req);
    if req.cookie("whoami").is_none() {
        res.add_cookie(
            &Cookie::build(
                "whoami",
                visitor.fetch_add(1, Ordering::Relaxed).to_string(),
            )
            .http_only(true)
            .finish(),
        )?;
    }
    Ok(res)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "debug");
    std::env::set_var("RUST_BACKTRACE", "1");
    env_logger::init();

    let key = Ed25519KeyPair::from_pkcs8_maybe_unchecked(
        pem::parse(
            std::fs::read("key")
                .expect("Must be able to read the ED25519 key.")
                .as_slice(),
        )
        .expect("Expected a PEM-encoded key.")
        .contents
        .as_slice(),
    )
    .expect("Couldn't parse the keypair.");
    let key = Data::new(Arc::new(key));
    let flag = std::env::args().nth(1).expect("Flag argument not found");
    let flag = Data::new(flag);

    let id_counter = Data::new(AtomicUsize::default());
    let challenges = Data::new(Arc::new(Mutex::new(CLruCache::<usize, Vec<u8>>::new(
        NonZeroUsize::new(1 << 16).unwrap(),
    ))));

    HttpServer::new(move || {
        App::new()
            .app_data(id_counter.clone())
            .app_data(challenges.clone())
            .app_data(key.clone())
            .app_data(flag.clone())
            .service(challenge)
            .service(get_flag)
            .service(static_files)
            .service(index)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}

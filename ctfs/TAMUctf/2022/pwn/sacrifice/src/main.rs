use once_cell::sync::Lazy;
use rand::distributions::{Alphanumeric, DistString};
use rand::Rng;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashSet;
use std::error::Error;
use std::process::Stdio;
use std::sync::Mutex;
use tokio::fs;
use tokio::process::Command;
use tokio::time::{self, Duration};
use warp::http::StatusCode;
use warp::Filter;

static POWS: Lazy<Mutex<HashSet<Pow>>> = Lazy::new(|| Mutex::new(HashSet::with_capacity(32)));
const MAX_SANDBOX_TIMEOUT: Duration = Duration::from_secs(10);
const MAX_POW_TIMEOUT: Duration = Duration::from_secs(60 * 5);

#[derive(Debug, Clone, PartialEq, Eq, Hash, Deserialize, Serialize)]
struct Pow {
    prefix: String,
    hardness: usize,
}

impl Pow {
    fn new() -> Self {
        let mut rng = rand::thread_rng();
        let prefix_len = rng.gen_range(24..=32);
        let prefix = Alphanumeric.sample_string(&mut rng, prefix_len);
        let chall = Self {
            prefix,
            hardness: rng.gen_range(23..=25),
        };
        let clone = chall.clone();
        let clone2 = chall.clone();
        POWS.lock().unwrap().insert(clone);
        tokio::spawn(async move {
            time::sleep(MAX_POW_TIMEOUT).await;
            POWS.lock().unwrap().remove(&clone2);
        });
        chall
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Deserialize, Serialize)]
struct Solve {
    pow: Pow,
    solve: String,
    src: String,
}

impl Solve {
    fn check_pow(&self) -> bool {
        if POWS.lock().unwrap().remove(&self.pow) {
            let mut hasher = Sha256::default();
            hasher.update(&self.solve);
            let digest = hasher.finalize();
            let digest = digest.as_slice();
            let bytes = self.pow.hardness / 8;
            let bits = (self.pow.hardness % 8) as u32;
            digest[..bytes].iter().all(|&x| x == 0)
                && digest[bytes].checked_shr(8 - bits).unwrap_or(0) == 0
        } else {
            false
        }
    }
}

async fn sandbox(src: &str, root: &str) -> Result<(), Box<dyn Error>> {
    fs::create_dir_all(format!("{root}/sandbox/src")).await?;
    fs::create_dir_all(format!("{root}/runner/src")).await?;
    fs::write(
        format!("{root}/sandbox/Cargo.toml"),
        r#"
[package]
name = "sandbox"
version = "0.1.0"
edition = "2021"

[dependencies]
std = { path = "../../../std-lol" }
    "#,
    )
    .await?;
    fs::write(
        format!("{root}/sandbox/src/lib.rs"),
        format!(
            r#"
#![no_std]
#![forbid(unsafe_code)]
mod user {{
    {src}
}}
pub use user::main;
    "#
        ),
    )
    .await?;
    fs::write(
        format!("{root}/runner/src/main.rs"),
        "fn main() { sandbox::main(); }",
    )
    .await?;
    let toml = format!("{root}/runner/Cargo.toml");
    fs::write(
        &toml,
        r#"
[package]
name = "runner"
version = "0.1.0"
edition = "2021"

[dependencies]
sandbox = { path = "../sandbox" }

[profile.dev]
incremental = false
    "#,
    )
    .await?;

    let mut child = Command::new("cargo")
        .arg("run")
        .arg("--manifest-path")
        .arg(&toml)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .kill_on_drop(true)
        .spawn()?;

    tokio::select! {
        _ = time::sleep(MAX_SANDBOX_TIMEOUT) => {
            child.kill().await?;
            Err("exceeded maximum timeout length".into())
        },
        status = child.wait() => {
            if !status?.success() {
                Err("child finished with non-zero exit code".into())
            } else {
                Ok(())
            }
        },
    }
}

#[tokio::main]
async fn main() {
    let files = warp::fs::dir("static");

    let pow = warp::path::path("pow")
        .and(warp::get())
        .map(|| warp::reply::json(&Pow::new()));

    let sacrifice = warp::path::path("sacrifice")
        .and(warp::post())
        .and(warp::body::content_length_limit(1024 * 2))
        .and(warp::body::json())
        .map(|solve: Solve| {
            // I don't like twitter
            if !solve.check_pow() || solve.src.contains('#') {
                StatusCode::BAD_REQUEST
            } else {
                tokio::spawn(async move {
                    let id = solve.pow.prefix;
                    let root = format!("runners/{id}");
                    if let Err(e) = sandbox(&solve.src, &root).await {
                        eprintln!("{}", e);
                    }
                    let _ = fs::remove_dir_all(&root).await;
                });
                StatusCode::OK
            }
        });

    warp::serve(files.or(pow).or(sacrifice))
        .run(([0, 0, 0, 0], 7777))
        .await;
}

extern crate core;

use tokio::io::{BufReader, AsyncBufReadExt, Lines};
use tokio::process::{Command, Child, ChildStdout, ChildStdin};
use tokio::io::AsyncWriteExt;
use std::process::Stdio;
use std::io::{self, BufRead, ErrorKind};
use serde::{Deserialize, Serialize};
use serde_with::base64::{Base64};
use serde_with::serde_as;
use std::io::{Error, Write};
use std::fs;


struct Authenticator {
    process: Child,
    stdin: ChildStdin,
    reader: Lines<BufReader<ChildStdout>>
}

impl Authenticator {
    async fn call(&mut self, rpc: &RPC) -> Result<Vec<u8>, Error> {
        self.stdin.write((serde_json::to_string(&rpc).unwrap() + "\n").as_ref()).await?;
        let resp_str = self.reader.next_line().await?.unwrap();

        let resp: RPCResp = serde_json::from_str(resp_str.as_str())?;
        if resp.success == false {
            return Err(Error::new(ErrorKind::Other, "unsuccessful"));
        }
        match resp.signature {
            Some(p) => Ok(p),
            None => Err(Error::new(ErrorKind::Other, "empty signature"))
        }
    }
}

async fn make_child(cmd: &str, args: &[&str], expected_hello: &str) -> Authenticator {
    let mut cmd = Command::new(cmd);
    cmd.stdout(Stdio::piped());
    cmd.stdin(Stdio::piped());

    let mut cmd_process = cmd.args(args).spawn().expect("failed to spawn command");
    let cmd_process_stdout = cmd_process.stdout.take().expect("child did not have a handle to stdout");
    let cmd_process_stdin = cmd_process.stdin.take().expect("child did not have a handle to stdin");

    let mut cmd_process_reader = BufReader::new(cmd_process_stdout).lines();
    let hello = cmd_process_reader.next_line().await.unwrap().unwrap();
    assert_eq!(hello, expected_hello);

    return Authenticator{process: cmd_process, stdin: cmd_process_stdin, reader: cmd_process_reader}
}

#[serde_as]
#[derive(Serialize, Deserialize)]
struct RPC {
    method: String,
    #[serde_as(as = "Base64")]
    message: Vec<u8>,
    signatures: Option<RPCSignature>,
}

#[serde_as]
#[derive(Serialize, Deserialize, Default)]
struct RPCSignature {
    #[serde_as(as = "Base64")]
    ecdsa: Vec<u8>,
    #[serde_as(as = "Base64")]
    hmac: Vec<u8>,
    #[serde_as(as = "Base64")]
    aes: Vec<u8>,
}

#[serde_as]
#[derive(Serialize, Deserialize)]
struct RPCResp {
    success: bool,
    #[serde_as(as = "Option<Base64>")]
    signature: Option<Vec<u8>>,
}

const FORBIDDEN: &str = "We the people, in order to get points, are kindly asking for flag";
const MAX_LEN: usize = 1337;
const POLYNOMIAL_BOUND: u16 = 512;
const NOPE: &str = "nope";
const OK: &str = "ok";

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Multi authenticator started");
    let cwd = "/jailed";
    let mut hmac_auth = make_child("python3", &[[cwd, "index.py"].join("/").as_str()], "HMAC authenticator started").await;
    let mut ecdsa_auth = make_child([cwd, "indexgo"].join("/").as_str(), &[], "ECDSA authenticator started").await;
    let mut aes_auth = make_child("node", &[[cwd, "index.js"].join("/").as_str()], "AES authenticator started").await;
    let flag = fs::read_to_string([cwd, "flag"].join("/").as_str()).expect("Can read flag");

    let mut counter: u16 = 0;
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        if counter >= POLYNOMIAL_BOUND {
            break;
        }
        counter += 1;

        let input = line.unwrap();
        let mut rpc: RPC = match serde_json::from_str(input.as_str()) {
            Ok(x) => x,
            Err(_) => {
                println!("{}", NOPE);
                continue
            }
        };

        if rpc.message.len() > MAX_LEN {
            println!("{}", NOPE);
            continue;
        }

        let mut is_forbidden = false;
        if rpc.message == FORBIDDEN.as_bytes() {
            is_forbidden = true;
        }

        if rpc.method == "backdoor" {
            rpc.method = "auth".to_string();
            let aes_signature = aes_auth.call(&rpc).await?;
            io::stdout().write(&aes_signature[..15])?;
            io::stdout().flush()?;

        } else if rpc.method == "auth" {
            if !rpc.signatures.is_none() {
                println!("{}", NOPE);
                continue;
            }

            if is_forbidden {
                println!("{}", NOPE);
                continue;
            }

            let mut signature: RPCSignature = RPCSignature {..Default::default()};

            let hmac_signature = hmac_auth.call(&rpc).await?;
            rpc.message.append(&mut hmac_signature.to_vec());
            signature.hmac = hmac_signature;

            let ecdsa_signature = ecdsa_auth.call(&rpc).await?;
            rpc.message.append(&mut ecdsa_signature.to_vec());
            signature.ecdsa = ecdsa_signature;

            let aes_signature = aes_auth.call(&rpc).await?;
            signature.aes = aes_signature;

            println!("{}", serde_json::to_string(&signature).unwrap());

        } else {
            rpc.method = "verify".to_string();
            let sigs = match &rpc.signatures {
                Some(sigs) => {
                    if sigs.ecdsa.len() == 0 || sigs.hmac.len() == 0 || sigs.aes.len() == 0 {
                        println!("{}", NOPE);
                        continue;
                    }
                    sigs
                }
                None => {
                    println!("{}", NOPE);
                    continue;
                }
            };

            let msg_copy = rpc.message;

            rpc.message = msg_copy.to_vec();
            rpc.message.append(&mut sigs.hmac.to_vec());
            rpc.message.append(&mut sigs.ecdsa.to_vec());
            if let Err(_) = aes_auth.call(&rpc).await {
                println!("{}", NOPE);
                continue;
            }

            rpc.message = msg_copy.to_vec();
            rpc.message.append(&mut sigs.hmac.to_vec());
            if let Err(_) = ecdsa_auth.call(&rpc).await {
                println!("{}", NOPE);
                continue;
            }

            rpc.message = msg_copy.to_vec();
            if let Err(_) = hmac_auth.call(&rpc).await {
                println!("{}", NOPE);
                continue;
            }

            if is_forbidden {
                println!("{}", flag);
                break;
            } else {
                println!("{}", OK);
            }
        }
    }

    drop(hmac_auth.stdin);
    drop(ecdsa_auth.stdin);
    drop(aes_auth.stdin);

    hmac_auth.process.wait().await?;
    ecdsa_auth.process.wait().await?;
    aes_auth.process.wait().await?;

    Ok(())
}
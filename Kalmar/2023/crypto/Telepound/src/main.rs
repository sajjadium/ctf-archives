// totally ordinary AES ;) ;) ;) ;)
use aes_frast::aes_core::key_schedule_encrypt256;
use aes_frast::{N_SUBKEYS_128BIT, N_SUBKEYS_192BIT, N_SUBKEYS_256BIT};

use rand::rngs::OsRng;
use rand::Rng;
use serde::de::Visitor;

use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::{fs, thread};

use serde::{Deserialize, Serialize};

use serde_big_array::BigArray;

const HELLO: &str = "TELEPOUND CHAT SERVICE^TM WITH CUSTOM MILITARY-GRADE ENCRYPTION.";
const HELLO_LEN: usize = HELLO.len();

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SecurityLevel {
    None,
    High,
    Super,
    Extreme
}

impl Serialize for SecurityLevel {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: serde::Serializer {
        let s: u8 = match self {
            SecurityLevel::None => b'N',
            SecurityLevel::High => b'H',
            SecurityLevel::Super => b'S',
            SecurityLevel::Extreme => b'X',
        };
        serializer.serialize_u8(s)
    }
}

impl <'de> Deserialize<'de> for SecurityLevel {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: serde::Deserializer<'de> {
        let s: char = char::deserialize(deserializer)?;
        match s {
            'X' => Ok(Self::Extreme),
            'S' => Ok(Self::Super),
            'H' => Ok(Self::High),
            _ => Ok(Self::None),
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Ping(
    #[serde(with = "BigArray")]
    [u8; HELLO_LEN]
);

impl Ping {
    fn new() -> Self {
        let mut bs: [u8; HELLO_LEN] = [0u8; HELLO_LEN];
        bs.copy_from_slice(HELLO.as_bytes());
        Self(bs)
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Ack {
    ok: bool,
    prefix: Vec<u8>
}

#[derive(Serialize, Deserialize, Debug)]
struct Msg {
    topic: String,
    body: String,
}

#[derive(Serialize, Deserialize)]
struct Content {}

#[derive(Debug)]
enum Request {
    Ping(Ping),
    Msg(Msg),
    Ack(Ack),
    Error
}

impl Serialize for Request {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: serde::Serializer {

        match self {
            Request::Ping(ping) => {
                (0u8, ping).serialize(serializer)
            }
            Request::Msg(bs) => {
                (1u8, bs).serialize(serializer)
            }
            Request::Ack(ack) => {
                (2u8, ack).serialize(serializer)
            }
            Request::Error => {
                255u8.serialize(serializer)
            }
        }
    }
}

struct RequestVisitor {}

impl <'de> Visitor<'de> for RequestVisitor {
    type Value = Request;

    fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
        formatter.write_str("love all around")
    }

    fn visit_seq<A>(self, mut seq: A) -> Result<Self::Value, A::Error>
        where
            A: serde::de::SeqAccess<'de>, {

        let n: Option<u8> = seq.next_element()?;

        match n {
            Some(0u8) => {
                Ok(
                    match seq.next_element()? {
                        Some(ping) => Self::Value::Ping(ping),
                        None => Self::Value::Error
                    }
                )
            },
            Some(1u8) => {
                Ok(
                    match seq.next_element()? {
                        Some(msg) => Self::Value::Msg(msg),
                        None => Self::Value::Error
                    }
                )
            },
            Some(2u8) => {
                Ok(
                    match seq.next_element()? {
                        Some(ack) => Self::Value::Ack(ack),
                        None => Self::Value::Error
                    }
                )
            }
            _ => Ok(Self::Value::Error),
        }        
    }
}

impl <'de> Deserialize<'de> for Request {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: serde::Deserializer<'de> {
        deserializer.deserialize_tuple(2, RequestVisitor{})        
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Enc {
    secl: SecurityLevel,
    cntr: (u64, u64),
    innr: Vec<u8>,
}

#[derive(Debug)]
struct Key {
    rnds: [u32; N_SUBKEYS_256BIT],
}

impl Key {
    #[inline(never)]
    fn new(key: [u8; 32]) -> Self {
        let mut rnds = [0u32; N_SUBKEYS_256BIT];
        key_schedule_encrypt256(&key[..], &mut rnds);
        Self { rnds }
    }

    #[inline(never)]
    fn apply(&self, sec: SecurityLevel, mut inpt: [u8; 16]) -> [u8; 16] {
        match sec {
            SecurityLevel::High => aes_frast::aes_core::block_encrypt128_inplace(
                &mut inpt,
                &self.rnds[..N_SUBKEYS_128BIT],
            ),
            SecurityLevel::Super => aes_frast::aes_core::block_encrypt192_inplace(
                &mut inpt,
                &self.rnds[..N_SUBKEYS_192BIT],
            ),
            SecurityLevel::Extreme => aes_frast::aes_core::block_encrypt256_inplace(
                &mut inpt,
                &self.rnds[..N_SUBKEYS_256BIT],
            ),
            SecurityLevel::None => {
                inpt =  [0u8; 16];
            },
        }
        inpt
    }

    #[inline(never)]
    fn crypt(&self, sec: SecurityLevel, mut cntr: (u64, u64), msg: &[u8]) -> Vec<u8> {
        let mut out: Vec<u8> = vec![];
        for chk in msg.chunks(16) {
            let mut cnt = [0u8; 16];
            cnt[..8].copy_from_slice(&cntr.0.to_le_bytes());
            cnt[8..].copy_from_slice(&cntr.1.to_le_bytes());
            let pad = self.apply(sec, cnt);
            for i in 0..chk.len() {
                out.push(pad[i] ^ chk[i]);
            }
            cntr.0 += 1;
        }
        out
    }

    fn enc<T: Serialize>(&self, secl: SecurityLevel, elem: &T) -> Enc {
        let bs = bincode::serialize(elem).unwrap();
        let cntr = rand::rngs::OsRng.gen();
        let innr = self.crypt(secl, cntr, &bs[..]);
        Enc { secl, cntr, innr }
    }

    fn dec(&self, enc: Enc) -> (SecurityLevel, Vec<u8>) {
        let pt = self.crypt(enc.secl, enc.cntr, &enc.innr[..]);
        (enc.secl, pt)
    }
}

struct Secure {
    conn: TcpStream,
    key: Key,
}

impl Secure {
    fn new(conn: TcpStream) -> Self {
        let key = OsRng.gen();
        let key = Key::new(key);
        Self { key, conn }
    }

    fn send(&mut self, secl: SecurityLevel, elem: &Request) -> Result<(), ()> {
        let enc = self.key.enc(secl, elem);
        let bs = bincode::serialize(&enc).unwrap();
        self.conn
            .write_all(&(bs.len() as u16).to_le_bytes())
            .map_err(|_err| ())?;
        self.conn.write_all(&bs).map_err(|_err| ())?;
        self.conn.flush().map_err(|_err| ())
    }

    fn recv(&mut self) -> Result<(SecurityLevel, Vec<u8>), ()> {
        // read buf
        let mut len: [u8; 2] = [0u8; 2];
        self.conn.read_exact(&mut len).map_err(|_err| ())?;
        let mut buf = vec![0u8; u16::from_le_bytes(len) as usize];
        self.conn.read_exact(&mut buf).map_err(|_err| ())?;

        // decrypt
        let enc: Enc = bincode::deserialize(&buf[..]).map_err(|_| ())?;
        Ok(self.key.dec(enc))
    }
}

fn handle(flag: String, conn: TcpStream) -> Result<(), ()> {
    let mut conn = Secure::new(conn);

    // send a hello to announce yourselves
    conn.send(
        SecurityLevel::None,
        &Request::Ping(Ping::new())
    )?;

    loop {
        let (secl, pt) = conn.recv()?;
        match bincode::deserialize(&pt[..]) {
            Ok(Request::Msg(msg)) => {
                let (stop, secl, resp) = match (secl, msg.topic.as_str()) {
                    (SecurityLevel::High, "killerdog") => {
                        (
                            false,
                            SecurityLevel::High, 
                            Msg {
                                topic: "killerdog".to_owned(),
                                body: "Sweet Scrum Master Monster and Dynamic DevOps Ninja here at Kalmar International Cyber Telecommunications Solution Systems. Kill'r is our Warmblooded Employee of the Month, Darling of Humanoid Resources and a Juggler of (Many) Balls.".to_owned()
                            }
                        )
                    },
                    (SecurityLevel::Super, "rot256") => {
                        (
                            false,
                            SecurityLevel::Super, 
                            Msg {
                                topic: "rot256".to_owned(),
                                body: "Idempotent Hacker Stuck in a Fixpoint. Author of Your Current Misery. Least Valued Employee of Every Month.".to_owned()
                            }
                        )
                    },
                    (SecurityLevel::Extreme, "flags")  => {
                        if msg.body == "Killerdogg (killer dog double G) here, got flags?" {
                            (
                                true,
                                SecurityLevel::Extreme, 
                                Msg {
                                    topic: "flags".to_owned(),
                                    body: format!("Cool man, take one: {}. Anyway gotta bounce.", flag)
                                }
                            )
                        } else {
                            (
                                true,
                                SecurityLevel::High, 
                                Msg {
                                    topic: "hacker detected".to_owned(),
                                    body: "abort connection immediately".to_owned()
                                }
                            )
                        }
                    },
                    (_, "flags") => {
                        (
                            false,
                            secl, 
                            Msg {
                                topic: "enc pls".to_owned(),
                                body: "dude switch on extreme military-grade encryption^TM! Someone might be listening...".to_owned()
                            }
                        )
                    }
                    (_, "CrYPtO") => {
                        (
                            true,
                            secl,
                            Msg {
                                topic: "btc".to_owned(),
                                body: "I love Bitcoin, it totally showed those bankers. Anyway gotta go pay my morgage.".to_owned()
                            }
                        )
                    }
                    (_, "crows") => {
                        (
                            false,
                            secl,
                            Msg {
                                topic: "birds".to_owned(),
                                body: "birds man, fuckin birds, silly goofs, love em <3".to_owned()
                            }
                        )
                    }
                    (_, "security") => {
                        let mut secl: SecurityLevel = if OsRng.gen() { SecurityLevel::Super } else { SecurityLevel::High };
                        if OsRng.gen::<u16>() == 0 {
                            secl = SecurityLevel::Extreme;
                        } 
                        (
                            false,
                            secl,
                            Msg {
                                topic: "security".to_owned(),
                                body: "Switchin channels what I'm all about...".to_owned()
                            }
                        )
                    }
                    _ => {
                        (
                            false,
                            secl,
                            Msg {
                                topic: msg.topic,
                                body: format!("\"{}\". Bro I totally agree", msg.body) 
                            }
                        )
                    }
                };
                conn.send(secl, &Request::Msg(resp))?;
                if stop {
                    return Ok(());
                }
            }
            Ok(Request::Ack(_)) => {
                println!("ack -- nice and useless");
            },
            Ok(Request::Ping(ping)) => {
                let mut ok: bool = true;
                for i in 0..HELLO_LEN {
                    if ping.0[i] != HELLO.as_bytes()[i] {
                        conn.send(
                            SecurityLevel::High,
                            &Request::Ack(Ack{
                                ok: false,
                                prefix: HELLO.as_bytes()[..i].to_owned()
                            })
                        )?;
                        ok = false;
                        break
                    }
                }
                if ok {
                    conn.send(
                        SecurityLevel::High,
                        &Request::Ack(Ack{
                            ok: true,
                            prefix: HELLO.as_bytes().to_owned()
                        })
                    )?;
                }
            }
            _err => {
                conn.send(
                    SecurityLevel::High,
                    &Request::Error
                )?;
            }
        }
    }
}

fn main() {
    println!("Initializing Telepound Secure Messaging");

    let flag = fs::read_to_string("./flag.txt").expect("need a flag");

    let ln = TcpListener::bind("0.0.0.0:13337").expect("cant bind");

    loop {
        match ln.accept() {
            Ok((conn, addr)) => {
                let flag = flag.clone();
                println!("some a**hole from {} just connected.", addr);
                thread::spawn(|| handle(flag, conn));
                ()
            }
            Err(_err) => break,
        }
    }
}
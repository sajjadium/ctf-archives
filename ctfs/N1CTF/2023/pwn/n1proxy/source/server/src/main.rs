use aes::cipher::block_padding::Pkcs7;
use aes::cipher::generic_array::GenericArray;
use aes::cipher::typenum::U16;
use aes::cipher::typenum::U32;
use aes::cipher::BlockDecryptMut;
use aes::cipher::BlockEncryptMut;
use aes::cipher::KeyIvInit;
use aes::Aes256;
use anyhow::anyhow;
use anyhow::Result;
use cbc::Decryptor;
use cbc::Encryptor;
use lazy_static::lazy_static;
use libc::c_char;
use libc::c_int;
use libc::c_void;
use libc::in_addr_t;
use libc::iovec;
use libc::mallopt;
use libc::memcmp;
use libc::msghdr;
use libc::read;
use libc::recvfrom;
use libc::recvmsg;
use libc::sendmsg;
use libc::sendto;
use libc::size_t;
use libc::sockaddr_in;
use libc::sockaddr_un;
use libc::socket;
use libc::ssize_t;
use libc::write;
use libc::AF_INET;
use libc::AF_UNIX;
use libc::MSG_CONFIRM;
use libc::MSG_WAITALL;
use libc::SOCK_DGRAM;
use libc::SOCK_STREAM;
use rand::thread_rng;
use rand::Rng;
use rsa::pkcs1v15;
use rsa::signature::SignatureEncoding;
use rsa::signature::Signer;
use rsa::signature::Verifier;
use rsa::traits::PublicKeyParts;
use rsa::Pkcs1v15Encrypt;
use rsa::RsaPrivateKey;
use rsa::RsaPublicKey;
use sha2::Digest;
use sha2::Sha256;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::mem;
use std::path::Path;
use std::process::exit;
use std::slice;
use std::sync::Arc;
use std::thread;

type Aes256CbcEnc = Encryptor<Aes256>;
type Aes256CbcDec = Decryptor<Aes256>;

const HELLO_MSG: &str = "n1proxy server v0.1";
const CLIENT_HELLO: &str = "n1proxy client v0.1";

const KEY_BITS: usize = 4096;
const MAX_STREAM: usize = 30;
const TOTAL_STREAM: usize = MAX_STREAM;

#[derive(Debug, Clone)]
struct SessionKey {
    key: Vec<u8>,
    iv: Vec<u8>,
}

impl SessionKey {
    pub fn to_bytes(&self) -> Vec<u8> {
        let mut res = self.key.clone();
        res.extend(self.iv.clone());
        res
    }
}

lazy_static! {
    static ref PRIV_KEY: Arc<RsaPrivateKey> = Arc::new({
        let mut rng = rand::thread_rng();
        RsaPrivateKey::new(&mut rng, KEY_BITS).expect("failed to generate a key")
    });
    static ref CLIENT_KEY: parking_lot::Mutex<HashMap<RsaPublicKey, SessionKey>> =
        parking_lot::Mutex::new(HashMap::new());
    static ref CLIENT_STREAM: parking_lot::Mutex<HashMap<RsaPublicKey, HashSet<i32>>> =
        parking_lot::Mutex::new(HashMap::new());
}

#[allow(dead_code)]
#[derive(Debug)]
enum ConnType {
    New = 0,
    Restore = 1,
    Renew = 2,
    Restart = 114514,
    Unknown = 3,
}

impl ConnType {
    pub fn from_le_bytes(data: &[u8]) -> ConnType {
        let data = u32::from_le_bytes(match data.try_into() {
            Ok(data) => data,
            Err(_) => return ConnType::Unknown,
        });
        match data {
            0 => ConnType::New,
            1 => ConnType::Restore,
            2 => ConnType::Renew,
            _ => ConnType::Unknown,
        }
    }
}
#[derive(Debug)]
enum ProxyType {
    Tcp = 0,
    Udp = 1,
    Sock = 2,
    Unknown = 3,
}
#[derive(Debug)]
enum ProxyStatus {
    Send = 0,
    Recv = 1,
    Conn = 2,
    Close = 3,
    Listen = 4,
    Unknown = 5,
}

impl ProxyType {
    pub fn from_le_bytes(data: &[u8]) -> ProxyType {
        let data = u32::from_le_bytes(match data.try_into() {
            Ok(data) => data,
            Err(_) => return ProxyType::Unknown,
        });
        match data {
            0 => ProxyType::Tcp,
            1 => ProxyType::Udp,
            2 => ProxyType::Sock,
            _ => ProxyType::Unknown,
        }
    }
}

impl ProxyStatus {
    pub fn from_le_bytes(data: &[u8]) -> ProxyStatus {
        let data = u32::from_le_bytes(match data.try_into() {
            Ok(data) => data,
            Err(_) => return ProxyStatus::Unknown,
        });
        match data {
            0 => ProxyStatus::Send,
            1 => ProxyStatus::Recv,
            2 => ProxyStatus::Conn,
            3 => ProxyStatus::Close,
            4 => ProxyStatus::Listen,
            _ => ProxyStatus::Unknown,
        }
    }
}

macro_rules! os_error {
    () => {
        Err(std::io::Error::last_os_error().into())
    };
}

extern "C" {
    fn inet_addr(__cp: *const c_char) -> in_addr_t;
}

#[inline(always)]
fn my_write(fd: c_int, buf: *const c_void, count: size_t) -> Result<ssize_t> {
    let res = unsafe { write(fd, buf, count) };
    if res < 0 {
        Err(anyhow!("Failed to write to socket"))
    } else {
        Ok(res)
    }
}

#[inline(always)]
fn my_read(fd: c_int, buf: *mut c_void, count: size_t) -> Result<ssize_t> {
    let res = unsafe { read(fd, buf, count) };
    if res < 0 {
        Err(anyhow!("Failed to read from socket"))
    } else {
        Ok(res)
    }
}

fn my_connect(target_ip: &str, target_port: u16) -> Result<i32> {
    let target_fd = unsafe { libc::socket(AF_INET, SOCK_STREAM, 0) };
    let target_ip = target_ip.to_owned() + "\0";

    let mut target: sockaddr_in = unsafe { mem::zeroed() };

    target.sin_family = libc::AF_INET as u16;

    target.sin_addr.s_addr = unsafe { inet_addr(target_ip.as_ptr() as *const _) };
    target.sin_port = target_port.to_be();

    let res = unsafe {
        libc::connect(
            target_fd,
            &target as *const _ as *const _,
            mem::size_of_val(&target) as u32,
        )
    };

    if res < 0 {
        return os_error!();
    }

    Ok(target_fd)
}

// record fd and target addr
lazy_static! {
    static ref UDP_TARGET: parking_lot::Mutex<HashMap<i32, sockaddr_in>> =
        parking_lot::Mutex::new(HashMap::new());
}

#[inline(always)]
fn my_new_udp_connect(target_ip: &str, target_port: u16) -> Result<i32> {
    let sockfd = unsafe { socket(AF_INET, SOCK_DGRAM, 0) };
    if sockfd <= 0 {
        return os_error!();
    }

    let mut server_addr: sockaddr_in = unsafe { mem::zeroed() };

    let target_ip = target_ip.to_owned() + "\0";
    server_addr.sin_family = AF_INET as u16;
    server_addr.sin_addr.s_addr = unsafe { inet_addr(target_ip.as_ptr() as *const _) };
    server_addr.sin_port = target_port.to_be();

    let res = unsafe {
        libc::connect(
            sockfd,
            &server_addr as *const _ as *const _,
            mem::size_of_val(&server_addr) as u32,
        )
    };

    if res < 0 {
        return os_error!();
    }

    UDP_TARGET.lock().insert(sockfd, server_addr);

    Ok(sockfd)
}

#[inline(always)]
fn my_sendto(fd: i32, msg: &[u8]) -> Result<isize> {
    let target = *UDP_TARGET
        .lock()
        .get(&fd)
        .ok_or_else(|| anyhow!("Invalid fd"))?;

    let res = unsafe {
        sendto(
            fd,
            msg.as_ptr() as *const _ as *const _,
            msg.len(),
            MSG_CONFIRM,
            &target as *const _ as *const _,
            mem::size_of_val(&target) as u32,
        )
    };

    if res < 0 {
        return os_error!();
    }

    Ok(res)
}

#[inline(always)]
fn my_recvfrom(fd: i32, recv_size: usize) -> Result<Vec<u8>> {
    let mut target = *UDP_TARGET
        .lock()
        .get(&fd)
        .ok_or_else(|| anyhow!("Invalid fd"))?;

    let mut res_msg = vec![0u8; recv_size];
    let mut addr_len = mem::size_of_val(&target) as u32;

    let recv_size = unsafe {
        recvfrom(
            fd,
            res_msg.as_mut_ptr() as *mut _,
            recv_size,
            MSG_WAITALL,
            &mut target as *mut _ as *mut _,
            &mut addr_len,
        )
    };
    if recv_size < 0 {
        return os_error!();
    }

    Ok(res_msg.to_vec())
}

const SOCKET_DIR: &str = "/tmp/n1proxy";

lazy_static! {
    static ref LISTEN_SOCK: parking_lot::Mutex<HashMap<String, (i32, Vec<i32>)>> =
        parking_lot::Mutex::new(HashMap::new());
}

fn hash_filename(path: &str, target_port: u16) -> String {
    Sha256::digest(format!("{}-{}", path, target_port))
        .iter()
        .map(|b| format!("{:02x}", b))
        .collect::<Vec<_>>()
        .join("")
}
#[inline(always)]
fn new_unix_socket_listen(path: &str, target_port: u16) -> Result<i32> {
    let socket_path = Path::new(SOCKET_DIR);
    if !socket_path.exists() {
        fs::create_dir_all(socket_path).expect("Failed to create socket dir");
    }

    let real_path = socket_path.join(hash_filename(path, target_port));

    println!("Socket path {:?}", real_path);

    let (sockfd, _) = LISTEN_SOCK
        .lock()
        .get(&real_path.as_os_str().to_string_lossy().to_string())
        .map(|f| {
            println!("cached fd");
            Ok(f.to_owned())
        })
        .unwrap_or_else(|| {
            println!("create new unix socket");
            let sockfd = unsafe { socket(AF_UNIX, SOCK_STREAM, 0) };
            if sockfd <= 0 {
                return os_error!();
            }
            let mut sock: sockaddr_un = unsafe { mem::zeroed() };

            sock.sun_family = AF_UNIX as u16;
            let path: String = real_path.as_os_str().to_string_lossy().to_string() + "\0";
            if path.len() > sock.sun_path.len() {
                return Err(anyhow!("Socket path too long"));
            }
            unsafe {
                libc::strcpy(sock.sun_path.as_mut_ptr(), path.as_ptr() as *const _);
            }
            let res = unsafe {
                libc::bind(
                    sockfd,
                    &sock as *const _ as *const _,
                    mem::size_of_val(&sock) as u32,
                )
            };

            if res < 0 {
                unsafe {
                    libc::close(sockfd);
                }
                println!("Failed to bind socket");
                return os_error!();
            }

            let res = unsafe { libc::listen(sockfd, 100) };
            if res < 0 {
                unsafe {
                    libc::close(sockfd);
                }
                println!("Failed listen socket");
                return os_error!();
            }
            Ok((sockfd, vec![]))
        })?;

    let client_fd = unsafe { libc::accept(sockfd, std::ptr::null_mut(), std::ptr::null_mut()) };
    if client_fd < 0 {
        unsafe {
            libc::close(sockfd);
        }
        return os_error!();
    }

    LISTEN_SOCK
        .lock()
        .entry(real_path.as_os_str().to_string_lossy().to_string())
        .or_insert((sockfd, vec![]))
        .1
        .append(&mut vec![client_fd]);

    Ok(client_fd)
}

#[inline(always)]
fn new_unix_socket_connect(path: &str, target_port: u16) -> Result<i32> {
    let sockfd = unsafe { socket(AF_UNIX, SOCK_STREAM, 0) };
    if sockfd <= 0 {
        return os_error!();
    }

    let mut sock: sockaddr_un = unsafe { mem::zeroed() };

    sock.sun_family = AF_UNIX as u16;
    let path = Path::new(SOCKET_DIR)
        .join(hash_filename(path, target_port))
        .to_string_lossy()
        .to_string()
        + "\0";

    println!("connect socket path {:?}", path);

    if path.len() > sock.sun_path.len() {
        return Err(anyhow!("Socket path too long"));
    }
    unsafe {
        libc::strcpy(sock.sun_path.as_mut_ptr(), path.as_ptr() as *const _);
    }

    let res = unsafe {
        libc::connect(
            sockfd,
            &sock as *const _ as *const _,
            mem::size_of_val(&sock) as u32,
        )
    };

    if res < 0 {
        unsafe {
            libc::close(sockfd);
        }
        return os_error!();
    }

    Ok(sockfd)
}

#[inline(always)]
fn my_send_msg(fd: i32, msg: &[u8]) -> Result<isize> {
    let mut iov = vec![iovec {
        iov_base: msg.as_ptr() as *mut _,
        iov_len: msg.len(),
    }];
    let m = msghdr {
        msg_name: std::ptr::null_mut(),
        msg_namelen: 0,
        msg_iov: iov.as_mut_ptr(),
        msg_iovlen: iov.len(),
        msg_control: std::ptr::null_mut(),
        msg_controllen: 0,
        msg_flags: 0,
    };
    let send_res = unsafe { sendmsg(fd, &m, 0) };

    if send_res < 0 {
        return os_error!();
    }
    Ok(send_res)
}

#[inline(always)]
fn my_recv_msg(fd: i32, recv_size: usize) -> Result<Vec<u8>> {
    let mut recv_iov = [iovec {
        iov_base: vec![0u8; recv_size].as_mut_ptr() as *mut _,
        iov_len: recv_size,
    }];
    let mut msg = msghdr {
        msg_name: std::ptr::null_mut(),
        msg_namelen: 0,
        msg_iov: recv_iov.as_mut_ptr(),
        msg_iovlen: 1,
        msg_control: std::ptr::null_mut(),
        msg_controllen: 0,
        msg_flags: 0,
    };
    let recv_sz = unsafe { recvmsg(fd, &mut msg, 0) };
    if recv_sz < 0 {
        return os_error!();
    }

    let res = unsafe { slice::from_raw_parts(recv_iov[0].iov_base as *const u8, recv_size) };
    Ok(res.to_vec())
}

#[inline(always)]
fn now_timestamp() -> u64 {
    let now = std::time::SystemTime::now();
    now.duration_since(std::time::UNIX_EPOCH)
        .expect("Time went backwards")
        .as_secs()
}

fn session_dec(keys: SessionKey, msg: &[u8]) -> Result<Vec<u8>> {
    if msg.len() % 16 != 0 {
        return Err(anyhow!("Invalid message length"));
    }

    let key = GenericArray::<_, U32>::from_slice(
        keys.key
            .get(0..32)
            .ok_or_else(|| anyhow!("Invalid key length {}", keys.key.len()))?,
    );
    let iv = GenericArray::<_, U16>::from_slice(
        keys.iv
            .get(0..16)
            .ok_or_else(|| anyhow!("Invalid iv length {}", keys.iv.len()))?,
    );
    let mut msg = msg.to_vec();

    let dec = match Aes256CbcDec::new(key, iv).decrypt_padded_mut::<Pkcs7>(&mut msg) {
        Ok(dec) => dec,
        Err(err) => return Err(anyhow!("Failed to decrypt message {}", err)),
    };

    Ok(dec.to_vec())
}

fn session_enc(keys: SessionKey, msg: &[u8]) -> Result<Vec<u8>> {
    let key = GenericArray::<_, U32>::from_slice(
        keys.key
            .get(0..32)
            .ok_or_else(|| anyhow!("Invalid key length {}", keys.key.len()))?,
    );
    let iv = GenericArray::<_, U16>::from_slice(
        keys.iv
            .get(0..16)
            .ok_or_else(|| anyhow!("Invalid iv length {}", keys.iv.len()))?,
    );
    let mut msg = msg.to_vec();
    let msg_len = msg.len();
    let padding_len = (16 - (msg_len % 16)) % 16;
    msg.extend(vec![padding_len as u8; padding_len]);

    let enc = match Aes256CbcEnc::new(key, iv).encrypt_padded_mut::<Pkcs7>(&mut msg, msg_len) {
        Ok(enc) => enc,
        Err(err) => return Err(anyhow!("Failed to encrypt message {}", err)),
    };

    Ok(enc.to_vec())
}

fn handle_client(stream_fd: i32) -> Result<()> {
    my_write(
        stream_fd,
        HELLO_MSG.as_ptr() as *const c_void,
        HELLO_MSG.len() as size_t,
    )?;

    let mut client_hello = [0; CLIENT_HELLO.len()];

    my_read(
        stream_fd,
        client_hello.as_mut_ptr() as *mut c_void,
        client_hello.len() as size_t,
    )?;

    let res = unsafe {
        memcmp(
            client_hello.as_ptr() as *const c_void,
            CLIENT_HELLO.as_ptr() as *const c_void,
            CLIENT_HELLO.len() as size_t,
        )
    };

    if res != 0 {
        return Err(anyhow!("Invalid client hello"));
    }

    println!("Client connected");

    let mut conn_type = vec![0; 4];
    my_read(
        stream_fd,
        conn_type.as_mut_ptr() as *mut c_void,
        conn_type.len() as size_t,
    )?;

    let conn_type = ConnType::from_le_bytes(&conn_type);

    println!("Connection type {:?}", conn_type);

    let pri_key = PRIV_KEY.as_ref().clone();
    let pub_key = RsaPublicKey::from(&pri_key);

    let pub_key_n = pub_key.n().to_bytes_be();
    let pub_key_e = pub_key.e().to_bytes_be();

    let key_exchange = vec![
        pub_key_n.len().to_le_bytes().to_vec(),
        pub_key_e.len().to_le_bytes().to_vec(),
        pub_key_n,
        pub_key_e,
    ]
    .concat();

    let signing_key = pkcs1v15::SigningKey::<Sha256>::new(pri_key.clone());

    let key_exchange_sign = signing_key.sign(&key_exchange).to_bytes();

    let key_exchange_sign = vec![
        key_exchange_sign.len().to_le_bytes().to_vec(),
        key_exchange_sign.to_vec(),
    ]
    .concat();

    println!("Sending key exchange");

    my_write(
        stream_fd,
        key_exchange_sign.as_ptr() as *const c_void,
        key_exchange_sign.len() as size_t,
    )?;

    my_write(
        stream_fd,
        key_exchange.as_ptr() as *const c_void,
        key_exchange.len() as size_t,
    )?;

    let mut client_msg_len = [0; 8];

    my_read(
        stream_fd,
        client_msg_len.as_mut_ptr() as *mut c_void,
        client_msg_len.len() as size_t,
    )?;

    let client_verify_len = u64::from_le_bytes(client_msg_len) as usize;

    println!("Client verify len {}", client_verify_len);

    let mut client_verify = vec![0; client_verify_len];

    my_read(
        stream_fd,
        client_verify.as_mut_ptr() as *mut c_void,
        client_verify.len() as size_t,
    )?;

    my_read(
        stream_fd,
        client_msg_len.as_mut_ptr() as *mut c_void,
        client_msg_len.len() as size_t,
    )?;

    let client_key_len = u64::from_le_bytes(client_msg_len) as usize;
    let mut client_key_n = vec![0; client_key_len];

    println!("Client key n len {}", client_key_len);

    my_read(
        stream_fd,
        client_key_n.as_mut_ptr() as *mut c_void,
        client_key_n.len() as size_t,
    )?;

    my_read(
        stream_fd,
        client_msg_len.as_mut_ptr() as *mut c_void,
        client_msg_len.len() as size_t,
    )?;

    let client_key_len = u64::from_le_bytes(client_msg_len) as usize;

    println!("Client key e len {}", client_key_len);

    let mut client_key_e = vec![0; client_key_len];

    my_read(
        stream_fd,
        client_key_e.as_mut_ptr() as *mut c_void,
        client_key_e.len() as size_t,
    )?;

    let client_key = RsaPublicKey::new(
        rsa::BigUint::from_bytes_be(&client_key_n),
        rsa::BigUint::from_bytes_be(&client_key_e),
    )?;

    let client_verify_key = pkcs1v15::VerifyingKey::<Sha256>::new(client_key.clone());
    let signature = pkcs1v15::Signature::try_from(&*client_verify)?;

    client_verify_key
        .verify(
            &vec![
                client_key_n.len().to_le_bytes().to_vec(),
                client_key_n,
                client_key_e.len().to_le_bytes().to_vec(),
                client_key_e,
            ]
            .concat(),
            &signature,
        )
        .map_err(|_| anyhow!("Invalid client key"))?;

    let session_key = match conn_type {
        ConnType::New | ConnType::Renew => {
            let session_key = SessionKey {
                key: thread_rng().gen::<[u8; 32]>().to_vec(),
                iv: thread_rng().gen::<[u8; 16]>().to_vec(),
            };
            CLIENT_KEY
                .lock()
                .insert(client_key.clone(), session_key.clone());

            println!("gen new key {:?}", session_key);

            let enc_key =
                client_key.encrypt(&mut thread_rng(), Pkcs1v15Encrypt, &session_key.to_bytes())?;

            let enc_time = client_key.encrypt(
                &mut thread_rng(),
                Pkcs1v15Encrypt,
                &now_timestamp().to_le_bytes(),
            )?;

            let new_session = vec![
                enc_key.len().to_le_bytes().to_vec(),
                enc_key,
                enc_time.len().to_le_bytes().to_vec(),
                enc_time,
            ]
            .concat();

            let new_session_sign = signing_key.sign(&new_session).to_bytes();

            let new_session_sign = vec![
                new_session_sign.len().to_le_bytes().to_vec(),
                new_session_sign.to_vec(),
            ]
            .concat();

            my_write(
                stream_fd,
                new_session_sign.as_ptr() as *const c_void,
                new_session_sign.len() as size_t,
            )?;

            my_write(
                stream_fd,
                new_session.as_ptr() as *const c_void,
                new_session.len() as size_t,
            )?;

            println!("Sending new session finished");

            session_key
        }
        ConnType::Restore => {
            let session_keys = CLIENT_KEY.lock();
            let session_key = session_keys
                .get(&client_key)
                .ok_or_else(|| anyhow!("Invalid client key"))?;
            session_key.clone()
        }
        ConnType::Unknown => {
            return Err(anyhow!("Invalid connection type"));
        }
        ConnType::Restart => {
            exit(0);
        }
    };

    let mut pre_conn = vec![0; 2048];

    let recv_res = my_read(
        stream_fd,
        pre_conn.as_mut_ptr() as *mut c_void,
        pre_conn.len() as size_t,
    )?;
    pre_conn.resize(recv_res as usize, 0);

    let pre_conn = session_dec(session_key.clone(), &pre_conn)?;

    if pre_conn.len() < 16 {
        return Err(anyhow!("Invalid pre connection data"));
    }

    let conn_type = ProxyType::from_le_bytes(&pre_conn[0..4]);
    let status = ProxyStatus::from_le_bytes(&pre_conn[4..8]);

    println!("Conn type {:?} status {:?}", conn_type, status);

    let signature = pkcs1v15::Signature::try_from(&pre_conn[8..])?;

    client_verify_key
        .verify(&pre_conn[0..8], &signature)
        .map_err(|_| anyhow!("Invalid client key"))?;

    let ok_msg = vec![0; 4];
    let signing_key = pkcs1v15::SigningKey::<Sha256>::new(pri_key.clone());
    let key_exchange_sign = signing_key.sign(&ok_msg).to_bytes();
    let ok_msg = vec![
        ok_msg,
        key_exchange_sign.len().to_le_bytes().to_vec(),
        key_exchange_sign.to_vec(),
    ]
    .concat();
    let ok_msg = session_enc(session_key.clone(), &ok_msg)?;

    my_write(
        stream_fd,
        ok_msg.as_ptr() as *const c_void,
        ok_msg.len() as size_t,
    )?;

    let res_msg = match status {
        ProxyStatus::Send => {
            let mut conn_data = vec![0; 2048];
            let recv_res = my_read(
                stream_fd,
                conn_data.as_mut_ptr() as *mut c_void,
                conn_data.len() as size_t,
            )?;

            conn_data.resize(recv_res as usize, 0);

            let conn_data = session_dec(session_key.clone(), &conn_data)?;

            if conn_data.len() < 32 {
                return Err(anyhow!("Invalid data"));
            }

            let target_fd = i32::from_le_bytes(conn_data[0..4].try_into()?);

            if CLIENT_STREAM
                .lock()
                .get(&client_key)
                .and_then(|fds| fds.contains(&target_fd).then_some(0))
                .is_none()
            {
                return Err(anyhow!("Invalid fd: {}", target_fd));
            }

            let mut send_data_size = usize::from_le_bytes(conn_data[4..12].try_into()?);

            let mut send_data = vec![];
            let mut remain_data = vec![];

            if send_data_size <= conn_data.len() - 12 {
                send_data.extend(conn_data[12..(12 + send_data_size)].to_vec());
                remain_data = conn_data[(12 + send_data_size)..].to_vec();
                if remain_data.len() < 512 {
                    let mut send_data_part = vec![0; 512];
                    let recv_res = my_read(
                        stream_fd,
                        send_data_part.as_mut_ptr() as *mut c_void,
                        send_data_part.len() as size_t,
                    )?;
                    send_data_part.resize(recv_res as usize, 0);
                    let send_data_part = session_dec(session_key.clone(), &send_data_part)?;
                    remain_data.extend(send_data_part);
                }
                send_data_size = 0;
            } else {
                send_data.extend(conn_data[12..].to_vec());
                send_data_size -= conn_data.len() - 12;
            }
            if send_data_size > 0 {
                // ensure read signature
                let mut send_data_part = vec![0; send_data_size + 0x2000];
                let recv_res = my_read(
                    stream_fd,
                    send_data_part.as_mut_ptr() as *mut c_void,
                    send_data_part.len() as size_t,
                )?;
                send_data_part.resize(recv_res as usize, 0);
                let send_data_part = session_dec(session_key.clone(), &send_data_part)?;
                send_data.extend(send_data_part[0..send_data_size].to_vec());
                remain_data.extend(send_data_part[send_data_size..].to_vec());
            }

            let signature = pkcs1v15::Signature::try_from(&*remain_data)?;

            client_verify_key
                .verify(
                    &vec![
                        target_fd.to_le_bytes().to_vec(),
                        send_data.len().to_le_bytes().to_vec(),
                        send_data.clone(),
                    ]
                    .concat(),
                    &signature,
                )
                .map_err(|_| anyhow!("Invalid client key"))?;

            println!("Send data to fd {} size {}", target_fd, send_data.len());

            let send_res = match conn_type {
                ProxyType::Tcp => my_write(
                    target_fd,
                    send_data.as_ptr() as *const c_void,
                    send_data.len() as size_t,
                )?,
                ProxyType::Udp => my_sendto(target_fd, &send_data)?,
                ProxyType::Sock => my_send_msg(target_fd, &send_data)?,
                ProxyType::Unknown => return Err(anyhow!("Invalid conn type")),
            };
            send_res.to_le_bytes().to_vec()
        }
        ProxyStatus::Recv => {
            let mut conn_data = vec![0; 2048];
            let recv_res = my_read(
                stream_fd,
                conn_data.as_mut_ptr() as *mut c_void,
                conn_data.len() as size_t,
            )?;

            conn_data.resize(recv_res as usize, 0);

            let conn_data = session_dec(session_key.clone(), &conn_data)?;

            if conn_data.len() < 32 {
                return Err(anyhow!("Invalid data"));
            }

            let target_fd = i32::from_le_bytes(conn_data[0..4].try_into()?);

            if CLIENT_STREAM
                .lock()
                .get(&client_key)
                .and_then(|fds| fds.contains(&target_fd).then_some(0))
                .is_none()
            {
                return Err(anyhow!("Invalid fd: {}", target_fd));
            }
            let recv_data_size = u64::from_le_bytes(conn_data[4..12].try_into()?);

            println!("Recv data from fd {} size {}", target_fd, recv_data_size);

            let signature = pkcs1v15::Signature::try_from(&conn_data[12..])?;

            client_verify_key
                .verify(&conn_data[0..12], &signature)
                .map_err(|_| anyhow!("Invalid client key"))?;

            let recv_data = match conn_type {
                ProxyType::Tcp => {
                    let mut recv_data = vec![0; recv_data_size as usize];

                    let recv_sz = my_read(
                        target_fd,
                        recv_data.as_mut_ptr() as *mut c_void,
                        recv_data.len() as size_t,
                    )?;
                    recv_data.resize(recv_sz as usize, 0);
                    recv_data
                }
                ProxyType::Udp => my_recvfrom(target_fd, recv_data_size as usize)?,
                ProxyType::Sock => my_recv_msg(target_fd, recv_data_size as usize)?,
                ProxyType::Unknown => return Err(anyhow!("Invalid conn type")),
            };

            println!(
                "succ recv data from fd {} size {}",
                target_fd,
                recv_data.len()
            );

            vec![recv_data.len().to_le_bytes().to_vec(), recv_data.to_vec()].concat()
        }
        ProxyStatus::Conn => {
            let mut conn_data = vec![0; 2048];
            let recv_res = my_read(
                stream_fd,
                conn_data.as_mut_ptr() as *mut c_void,
                conn_data.len() as size_t,
            )?;
            conn_data.resize(recv_res as usize, 0);

            let conn_data = session_dec(session_key.clone(), &conn_data)?;

            if conn_data.len() < 64 {
                return Err(anyhow!("Invalid pre connection data"));
            }

            let target_host_len = u32::from_le_bytes(conn_data[0..4].try_into()?);
            let target_host =
                String::from_utf8(conn_data[4..(4 + target_host_len) as usize].to_vec())?;

            println!(
                "Target host len {:?}",
                conn_data[4..(4 + target_host_len) as usize].to_vec()
            );

            let mut next_index = 4 + target_host_len as usize;

            let target_port =
                u16::from_le_bytes(conn_data[next_index..(next_index + 2)].try_into()?);
            next_index += 2;

            println!(
                "Target host {} {} port {}",
                target_host_len, target_host, target_port
            );

            let signature = pkcs1v15::Signature::try_from(&conn_data[next_index..])?;

            client_verify_key
                .verify(&conn_data[0..next_index], &signature)
                .map_err(|_| anyhow!("Invalid client key"))?;

            let conn_fd = match conn_type {
                ProxyType::Tcp => my_connect(&target_host, target_port)?,
                ProxyType::Udp => my_new_udp_connect(&target_host, target_port)?,
                ProxyType::Sock => new_unix_socket_connect(&target_host, target_port)?,
                ProxyType::Unknown => return Err(anyhow!("Invalid conn type")),
            };

            let mut lock = CLIENT_STREAM.lock();
            let total_stream_count = lock.values().map(|fds| fds.len()).sum::<usize>();

            if total_stream_count >= TOTAL_STREAM {
                unsafe {
                    libc::close(conn_fd);
                }
                return Err(anyhow!("Too many streams"));
            }

            let client_streams = lock.entry(client_key).or_insert_with(HashSet::new);

            if client_streams.len() >= MAX_STREAM {
                unsafe {
                    libc::close(conn_fd);
                }
                return Err(anyhow!("Too many streams"));
            }

            client_streams.insert(conn_fd);
            println!("New conn fd {}", conn_fd);
            conn_fd.to_le_bytes().to_vec()
        }
        ProxyStatus::Close => {
            let mut conn_data = vec![0; 2048];
            let recv_res = my_read(
                stream_fd,
                conn_data.as_mut_ptr() as *mut c_void,
                conn_data.len() as size_t,
            )?;
            conn_data.resize(recv_res as usize, 0);

            let conn_data = session_dec(session_key.clone(), &conn_data)?;

            if conn_data.len() < 32 {
                return Err(anyhow!("Invalid pre connection data"));
            }

            let target_fd = i32::from_le_bytes(conn_data[0..4].try_into()?);

            let signature = pkcs1v15::Signature::try_from(&conn_data[4..])?;

            client_verify_key
                .verify(&conn_data[0..4], &signature)
                .map_err(|_| anyhow!("Invalid client key"))?;

            let mut lock = CLIENT_STREAM.lock();

            let client_streams = lock.entry(client_key).or_insert_with(HashSet::new);

            if client_streams.contains(&target_fd) {
                unsafe {
                    libc::close(target_fd);
                }
                client_streams.remove(&target_fd);
            }

            match conn_type {
                ProxyType::Udp => {
                    UDP_TARGET.lock().remove(&target_fd);
                }
                ProxyType::Sock => {
                    let mut socks = LISTEN_SOCK.lock();
                    socks.iter_mut().for_each(|(k, (i, v))| {
                        v.retain(|f| *f != target_fd);
                        if v.is_empty() {
                            unsafe {
                                libc::close(*i);
                            }
                            fs::remove_file(k).ok();
                        }
                    });
                    socks.retain(|_, (_, v)| !v.is_empty());
                }

                _ => (),
            };

            0u32.to_le_bytes().to_vec()
        }
        ProxyStatus::Listen => {
            let mut conn_data = vec![0; 2048];
            let recv_res = my_read(
                stream_fd,
                conn_data.as_mut_ptr() as *mut c_void,
                conn_data.len() as size_t,
            )?;
            conn_data.resize(recv_res as usize, 0);

            let conn_data = session_dec(session_key.clone(), &conn_data)?;

            if conn_data.len() < 64 {
                return Err(anyhow!("Invalid pre connection data"));
            }

            let target_host_len = u32::from_le_bytes(conn_data[0..4].try_into()?);
            let target_host =
                String::from_utf8(conn_data[4..(4 + target_host_len) as usize].to_vec())?;

            let mut next_index = 4 + target_host_len as usize;

            let target_port =
                u16::from_le_bytes(conn_data[next_index..(next_index + 2)].try_into()?);
            next_index += 2;

            let signature = pkcs1v15::Signature::try_from(&conn_data[next_index..])?;

            client_verify_key
                .verify(&conn_data[0..next_index], &signature)
                .map_err(|_| anyhow!("Invalid client key"))?;

            let conn_fd = match conn_type {
                ProxyType::Sock => new_unix_socket_listen(&target_host, target_port)?,
                _ => return Err(anyhow!("Invalid conn type")),
            };

            let mut lock = CLIENT_STREAM.lock();
            let total_stream_count = lock.values().map(|fds| fds.len()).sum::<usize>();

            if total_stream_count >= TOTAL_STREAM {
                unsafe {
                    libc::close(conn_fd);
                }
                return Err(anyhow!("Too many streams"));
            }

            let client_streams = lock.entry(client_key).or_insert_with(HashSet::new);

            if client_streams.len() >= MAX_STREAM {
                unsafe {
                    libc::close(conn_fd);
                }
                return Err(anyhow!("Too many streams"));
            }

            client_streams.insert(conn_fd);
            println!("New listen fd {}", conn_fd);
            conn_fd.to_le_bytes().to_vec()
        }
        ProxyStatus::Unknown => {
            return Err(anyhow!("Invalid conn type"));
        }
    };

    let signing_key = pkcs1v15::SigningKey::<Sha256>::new(pri_key);

    let key_exchange_sign = signing_key.sign(&res_msg).to_bytes();

    let res_msg = vec![res_msg, key_exchange_sign.to_vec()].concat();

    let res_msg = session_enc(session_key, &res_msg)?;

    my_write(stream_fd, res_msg.as_ptr() as *const c_void, res_msg.len())?;

    Ok(())
}

fn main() -> Result<()> {
    // make this easier :)
    unsafe {
        mallopt(libc::M_ARENA_MAX, 1);
    }

    let port = env::args().nth(1).unwrap_or("8080".to_string());
    let server_fd = unsafe { libc::socket(AF_INET, SOCK_STREAM, 0) };
    println!("n1proxy server listening on port {}", port);

    let mut server: sockaddr_in = unsafe { mem::zeroed() };

    server.sin_family = libc::AF_INET as u16;
    server.sin_addr.s_addr = libc::INADDR_ANY;
    server.sin_port = port.parse::<u16>()?.to_be();

    let socket_opt_res = unsafe {
        libc::setsockopt(
            server_fd,
            libc::SOL_SOCKET,
            libc::SO_REUSEADDR,
            &1 as *const _ as *const _,
            mem::size_of_val(&1) as u32,
        )
    };
    if socket_opt_res < 0 {
        panic!(
            "Failed to set socket options {:?}",
            std::io::Error::last_os_error()
        );
    }

    let bind_result = unsafe {
        libc::bind(
            server_fd,
            &server as *const _ as *const _,
            mem::size_of_val(&server) as u32,
        )
    };
    if bind_result < 0 {
        panic!(
            "Failed to bind socket {:?}",
            std::io::Error::last_os_error()
        );
    }

    let listen_result = unsafe { libc::listen(server_fd, 5) };

    if listen_result < 0 {
        panic!(
            "Failed to listen on socket {:?}",
            std::io::Error::last_os_error()
        );
    }

    loop {
        let client_fd =
            unsafe { libc::accept(server_fd, std::ptr::null_mut(), std::ptr::null_mut()) };
        if client_fd < 0 {
            break;
        }
        thread::spawn(move || {
            println!("New client connected");
            handle_client(client_fd).unwrap_or_else(|err| {
                eprintln!("Error: {}", err);
                let err_msg = format!("error : {}", err);
                my_write(client_fd, err_msg.as_ptr() as *const c_void, err_msg.len()).ok();
            });
            unsafe { libc::close(client_fd) };
            println!("Client disconnected")
        });
    }

    Ok(())
}

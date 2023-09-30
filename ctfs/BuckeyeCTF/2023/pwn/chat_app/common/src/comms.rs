
// Communication code

use tokio::net::{TcpStream, TcpListener, tcp::{OwnedReadHalf, OwnedWriteHalf}};
use tokio::io::AsyncWriteExt;
use tokio::io::AsyncReadExt;

use std::sync::{Arc};
use tokio::sync::RwLock;
use std::sync::mpsc::{channel, Sender, Receiver};

use crate::*;

async fn client_recv_loop(mut stream: OwnedReadHalf, channel: Sender<Message>) -> Result<(), Box<dyn Error>> {
    loop {
        let mut header = [0u8; 9];
        stream.read_exact(&mut header).await?;

        let pkt_type = header[0];
        let pkt_len = u64::from_le_bytes(header[1..9].try_into().unwrap());

        let message = match pkt_type {
            0 => {
                if pkt_len != std::mem::size_of::<NetPing>() as u64 {
                    println!("Received invalid ping packet");
                    continue;
                }
                let mut body = [0u8; std::mem::size_of::<NetPing>()];
                stream.read_exact(&mut body).await?;
                Message::try_from(unsafe { std::mem::transmute::<_, NetPing>(body) })
            },
            1 => {
                if pkt_len != std::mem::size_of::<NetJoin>() as u64 {
                    println!("Received invalid join packet");
                    continue;
                }
                let mut body = [0u8; std::mem::size_of::<NetJoin>()];
                stream.read_exact(&mut body).await?;
                Message::try_from(unsafe { std::mem::transmute::<_, NetJoin>(body) })
            },
            2 => {
                if pkt_len != std::mem::size_of::<NetFriendRequest>() as u64 {
                    println!("Received invalid friend request packet");
                    continue;
                }
                let mut body = [0u8; std::mem::size_of::<NetFriendRequest>()];
                stream.read_exact(&mut body).await?;
                Message::try_from(unsafe { std::mem::transmute::<_, NetFriendRequest>(body) })
            },
            3 => {
                if pkt_len != std::mem::size_of::<NetChatMessage>() as u64 {
                    println!("Received invalid chat message packet");
                    continue;
                }
                let mut body = [0u8; std::mem::size_of::<NetChatMessage>()];
                stream.read_exact(&mut body).await?;
                Message::try_from(unsafe { std::mem::transmute::<_, NetChatMessage>(body) })
            },
            4 => {
                if pkt_len != std::mem::size_of::<NetReaction>() as u64 {
                    println!("Received invalid reaction packet");
                    continue;
                }
                let mut body = [0u8; std::mem::size_of::<NetReaction>()];
                stream.read_exact(&mut body).await?;
                Message::try_from(unsafe { std::mem::transmute::<_, NetReaction>(body) })
            },
            _ => {
                println!("Received unknown packet type {}", pkt_type);
                Err("Unknown packet type")
            }
        };

        if let Ok(message) = message {
            channel.send(message).unwrap();
        }
    }
}

pub async fn client_send_loop(mut stream: OwnedWriteHalf, channel: Receiver<Message>) -> Result<(), Box<dyn Error>> {
    loop {
        let message = channel.recv()?;
        let (pkt_type, pkt_len, body) = match &message {
            Message::Ping(_, _) => {
                if let Ok(body) = NetPing::try_from(message) {
                    (
                        0,
                        std::mem::size_of::<NetPing>() as u64,
                        Vec::from(unsafe { std::mem::transmute::<_, [u8; std::mem::size_of::<NetPing>()]>(body) })
                    )
                } else { continue; }
            },
            Message::Join(_) => {
                if let Ok(body) = NetJoin::try_from(message) {
                    (
                        1,
                        std::mem::size_of::<NetJoin>() as u64,
                        Vec::from(unsafe { std::mem::transmute::<_, [u8; std::mem::size_of::<NetJoin>()]>(body) })
                    )
                } else { continue; }
            },
            Message::FriendRequest(_, _) => {
                if let Ok(body) = NetFriendRequest::try_from(message) {
                    (
                        2,
                        std::mem::size_of::<NetFriendRequest>() as u64,
                        Vec::from(unsafe { std::mem::transmute::<_, [u8; std::mem::size_of::<NetFriendRequest>()]>(body) })
                    )
                } else { continue; }
            },
            Message::Chat(_) => {
                if let Ok(body) = NetChatMessage::try_from(message) {
                    (
                        3,
                        std::mem::size_of::<NetChatMessage>() as u64,
                        Vec::from(unsafe { std::mem::transmute::<_, [u8; std::mem::size_of::<NetChatMessage>()]>(body) })
                    )
                } else { continue; }
            },
            Message::React(_) => {
                if let Ok(body) = NetReaction::try_from(message) {
                    (
                        4,
                        std::mem::size_of::<NetReaction>() as u64,
                        Vec::from(unsafe { std::mem::transmute::<_, [u8; std::mem::size_of::<NetReaction>()]>(body) })
                    )
                } else { continue; }
            },
            _ => { continue; }
        };
        stream.write_all(&[pkt_type]).await?;
        stream.write_all(&pkt_len.to_le_bytes()).await?;
        stream.write_all(&body).await?;
    }
}

pub async fn start_client(server: String) -> (Receiver<Message>, Sender<Message>) {
    let stream = TcpStream::connect(server).await.expect("Failed to connect to server");
    let (stream_r, stream_w) = stream.into_split();

    let (r_tx, r_rx) = channel(); // receive from server
    let (s_tx, s_rx) = channel(); // send to server
    tokio::spawn(async move {
        match client_recv_loop(stream_r, r_tx).await {
            Ok(_) => {},
            Err(e) => {
                println!("Error in client_recv_loop: {:?}", e);
            }

        }
    });
    tokio::spawn(async move {
        client_send_loop(stream_w, s_rx).await;
    });
    (r_rx, s_tx)
}

struct Chatroom {
    users: Vec<OwnedWriteHalf>,
}

async fn server_handle_connection(mut socket: OwnedReadHalf, chatroom: Arc<RwLock<Chatroom>>) -> std::io::Result<()> {
    loop {
        let mut header = [0u8; 9];
        socket.read_exact(&mut header).await?;

        let pkt_type = header[0];
        let pkt_len = usize::from_le_bytes(header[1..9].try_into().unwrap());

        let mut body = vec![0; pkt_len];
        socket.read_exact(&mut body).await?;

        match pkt_type {
            0 | 1 | 2 | 3 | 4 => {
                for user in chatroom.write().await.users.iter_mut() {
                    let _ = user.write_all(&header).await;
                    let _ = user.write_all(&body).await;
                }
            }
            _ => {
                println!("Received unknown packet type {}", pkt_type);
            }
        }
    }
}

async fn server_loop(port: usize) -> std::io::Result<()> {
    let mut listener = TcpListener::bind(format!("0.0.0.0:{}", port)).await?;
    println!("Listening on port {}", port);

    let chatroom = Arc::new(RwLock::new(Chatroom {
        users: Vec::new()
    }));

    loop {
        let (mut stream, _) = listener.accept().await?;
        println!("New connection from {:?}", stream.peer_addr());
        let (stream_r, stream_w) = stream.into_split();
        chatroom.write().await.users.push(stream_w);

        let cloned_chatroom = chatroom.clone();
        tokio::spawn(async move {
            server_handle_connection(stream_r, cloned_chatroom).await
        });
    }
}

pub async fn start_server(port: usize) -> std::io::Result<()> {
    server_loop(port).await
}
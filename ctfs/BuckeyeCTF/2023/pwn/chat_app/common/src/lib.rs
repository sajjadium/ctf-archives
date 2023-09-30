use std::error::Error;
use chrono::{DateTime, Utc};

pub mod comms;

pub const NUM_REACTIONS: usize = 4;

// Internal types (not sent over network)

#[derive(Debug)]
pub enum Message {
    Ping([u8; 32], bool),
    Join(String),
    FriendRequest(String, String),
    Chat(ChatMessage),
    React(Reaction),
}

#[derive(Debug)]
pub struct ChatMessage {
    pub id: usize,
    pub timestamp: i64,
    pub author: String,
    pub content: String,
    pub is_super: bool
}

#[derive(Copy, Clone, Debug, PartialEq)]
pub enum ReactionType {
    Like,
    Love,
    Haha,
    Wow,
    Pepega
}

#[derive(Debug)]
pub struct Reaction {
    pub target_id: usize,
    pub timestamp: i64,
    pub author: String,
    pub reaction_type: ReactionType
}

// Safe repr(C) types used for serialization -- sent over network

#[repr(C)]
pub(crate) struct NetChatMessage {
    pub id: usize,
    pub timestamp: i64,
    pub author: [u8; 32],
    pub content: [u8; 256],
    pub is_super: bool,
}

#[repr(C)]
pub(crate) struct NetReaction {
    pub target_id: usize,
    pub timestamp: i64,
    pub author: [u8; 32],
    pub reaction_type: ReactionType
}

#[repr(C)]
pub(crate) struct NetPing {
    pub data: [u8; 32],
    pub should_reply: bool
}

#[repr(C)]
pub(crate) struct NetJoin {
    pub name: [u8; 32]
}

#[repr(C)]
pub(crate) struct NetFriendRequest {
    pub from: [u8; 32],
    pub to: [u8; 32]
}

// Deserialization code (implement TryFrom)

fn trimmed_string_from_bytes(bytes: &[u8]) -> String {
    let mut trimmed = bytes.to_vec();
    for i in 0..trimmed.len() {
        if trimmed[i] == 0 {
            trimmed.truncate(i);
            break;
        }
    }
    unsafe { String::from_utf8_unchecked(trimmed) }
}

impl TryFrom<NetChatMessage> for Message {
    type Error = &'static str;

    fn try_from(value: NetChatMessage) -> Result<Self, Self::Error> {
        let author = trimmed_string_from_bytes(&value.author);
        let content = trimmed_string_from_bytes(&value.content);

        Ok(Message::Chat(ChatMessage {
            id: value.id,
            timestamp: value.timestamp,
            author,
            content,
            is_super: value.is_super,
        }))
    }
}

impl TryFrom<NetReaction> for Message {
    type Error = &'static str;

    fn try_from(value: NetReaction) -> Result<Self, Self::Error> {
        let author = trimmed_string_from_bytes(&value.author);

        Ok(Message::React(Reaction {
            target_id: value.target_id,
            timestamp: value.timestamp,
            author,
            reaction_type: value.reaction_type,
        }))
    }
}

impl TryFrom<NetPing> for Message {
    type Error = &'static str;

    fn try_from(value: NetPing) -> Result<Self, Self::Error> {
        Ok(Message::Ping(value.data, value.should_reply))
    }
}

impl TryFrom<NetJoin> for Message {
    type Error = &'static str;

    fn try_from(value: NetJoin) -> Result<Self, Self::Error> {
        let name = trimmed_string_from_bytes(&value.name);

        Ok(Message::Join(name))
    }
}

impl TryFrom<NetFriendRequest> for Message {
    type Error = &'static str;

    fn try_from(value: NetFriendRequest) -> Result<Self, Self::Error> {
        let name1 = trimmed_string_from_bytes(&value.from);
        let name2 = trimmed_string_from_bytes(&value.to);

        Ok(Message::FriendRequest(name1, name2))
    }
}

// Serialization code

impl TryFrom<Message> for NetChatMessage {
    type Error = &'static str;

    fn try_from(value: Message) -> Result<Self, Self::Error> {
        match value {
            Message::Chat(msg) => {
                let mut encoded_author = [0u8; 32];
                let mut encoded_content = [0u8; 256];
                if msg.author.len() > encoded_author.len() || msg.content.len() > encoded_content.len() {
                    return Err("Too long");
                }

                encoded_author[..msg.author.len()].copy_from_slice(msg.author.as_bytes());
                encoded_content[..msg.content.len()].copy_from_slice(msg.content.as_bytes());

                Ok(NetChatMessage {
                    id: msg.id,
                    timestamp: msg.timestamp,
                    author: encoded_author,
                    content: encoded_content,
                    is_super: msg.is_super
                })
            },
            _ => Err("Invalid message type")
        }
    }
}

impl TryFrom<Message> for NetJoin {
    type Error = &'static str;

    fn try_from(value: Message) -> Result<Self, Self::Error> {
        match value {
            Message::Join(name) => {
                let mut encoded_name = [0u8; 32];
                if name.len() > encoded_name.len() {
                    return Err("Too long");
                }
                encoded_name[..name.len()].copy_from_slice(name.as_bytes());

                Ok(NetJoin {
                    name: encoded_name
                })
            },
            _ => Err("Invalid message type")
        }
    }
}

impl TryFrom<Message> for NetFriendRequest {
    type Error = &'static str;

    fn try_from(value: Message) -> Result<Self, Self::Error> {
        match value {
            Message::FriendRequest(name1, name2) => {
                let mut encoded_name1 = [0u8; 32];
                let mut encoded_name2 = [0u8; 32];
                if name1.len() > encoded_name1.len() || name2.len() > encoded_name2.len() {
                    return Err("Too long");
                }
                encoded_name1[..name1.len()].copy_from_slice(name1.as_bytes());
                encoded_name2[..name2.len()].copy_from_slice(name2.as_bytes());

                Ok(NetFriendRequest {
                    from: encoded_name1,
                    to: encoded_name2
                })
            },
            _ => Err("Invalid message type")
        }
    }
}

impl TryFrom<Message> for NetPing {
    type Error = &'static str;

    fn try_from(value: Message) -> Result<Self, Self::Error> {
        match value {
            Message::Ping(data, should_reply) => {
                Ok(NetPing {
                    data,
                    should_reply
                })
            },
            _ => Err("Invalid message type")
        }
    }
}

impl TryFrom<Message> for NetReaction {
    type Error = &'static str;

    fn try_from(value: Message) -> Result<Self, Self::Error> {
        match value {
            Message::React(reaction) => {
                let mut encoded_author = [0u8; 32];
                if reaction.author.len() > encoded_author.len() {
                    return Err("Too long");
                }
                encoded_author[..reaction.author.len()].copy_from_slice(reaction.author.as_bytes());

                Ok(NetReaction {
                    target_id: reaction.target_id,
                    timestamp: reaction.timestamp,
                    author: encoded_author,
                    reaction_type: reaction.reaction_type
                })
            },
            _ => Err("Invalid message type")
        }
    }
}
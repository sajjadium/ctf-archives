use chat_common::comms::*;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let port = std::env::args().nth(1).unwrap().parse::<usize>().unwrap();
    start_server(port).await;
    Ok(())
}

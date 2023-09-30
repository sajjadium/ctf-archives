use std::error::Error;
mod tui;

#[tokio::main(flavor = "multi_thread", worker_threads = 6)]
async fn main() -> Result<(), Box<dyn Error>> {
    tui::tui_main().await
}

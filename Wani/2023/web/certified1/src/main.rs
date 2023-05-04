mod handler;
mod process_image;

use axum::routing::{get, post};
use axum::Router;
use std::net::SocketAddr;
use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let addr = std::env::var("LISTEN_ADDR")
        .map(|x| x.parse().unwrap())
        .unwrap_or(SocketAddr::from(([127, 0, 0, 1], 3000)));

    let app = Router::new()
        .route("/", get(handler::index::handle_index))
        .route("/create", post(handler::create::handle_create))
        .route("/view/:id", get(handler::view::handle_view))
        .layer(TraceLayer::new_for_http());

    tracing::info!("Listening on http://{}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

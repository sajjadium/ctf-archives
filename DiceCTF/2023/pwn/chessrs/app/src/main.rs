use axum::{
    http::{
        header::{HeaderMap, HeaderName, HeaderValue},
        Request,
    },
    middleware::{self, Next},
    response::IntoResponse,
    Router,
};
use axum_extra::routing::SpaRouter;
use std::net::SocketAddr;

async fn cache_mw<B>(req: Request<B>, next: Next<B>) -> (HeaderMap, impl IntoResponse) {
    let res = next.run(req).await;

    let mut headers = HeaderMap::new();
    headers.insert(
        HeaderName::from_static("cache-control"),
        HeaderValue::from_static("max-age=604800"),
    );

    (headers, res)
}

#[tokio::main]
async fn main() {
    let port: u16 = std::env::var("PORT")
        .unwrap_or_else(|_| "1337".to_string())
        .parse()
        .expect("Invalid PORT variable");

    let spa = SpaRouter::new("/", "static");
    let app = Router::new()
        .layer(middleware::from_fn(cache_mw))
        .merge(spa);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("pwn/chessrs listening on http://localhost:{}", port);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

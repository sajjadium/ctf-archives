use axum::Router;
use axum_extra::routing::SpaRouter;
use clokwerk::{Scheduler, TimeUnits};
use std::time::Duration;
use std::{env, net::SocketAddr};
use tower_cookies::CookieManagerLayer;

mod auth;
mod routes;
mod utils;

#[tokio::main]
async fn main() {
    let spa = SpaRouter::new("/assets", "static");

    let app = Router::new()
        .merge(spa)
        .nest("/api/", routes::api::router())
        .layer(CookieManagerLayer::new());

    let mut port = 1337;
    if let Ok(val) = env::var("PORT") {
        port = val.parse().unwrap()
    }

    let mut scheduler = Scheduler::new();
    scheduler.every(15.minutes()).run(|| {
        println!("[!] clearing DB"); // stop in-memory DB from growing too large :)
        utils::DB.clear();
        utils::SESSIONS.clear();
    });
    let _thread_handle = scheduler.watch_thread(Duration::from_millis(100));

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("rustshop listening on http://localhost:{}", port);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

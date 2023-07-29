use axum::{middleware, Extension, Router};
use axum_sessions::{async_session::CookieStore, SessionLayer};
use clokwerk::{Scheduler, TimeUnits};
use rand::Rng;
use std::net::SocketAddr;
use tera::Tera;
use tower_http::services::ServeDir;

mod db;
mod routes;
mod utils;

#[tokio::main]
async fn main() {
    let store = CookieStore::new();
    let secret: [u8; 64] = std::env::var("SECRET")
        .map(|p| p.as_bytes().try_into().expect("SECRET must be 64 bytes"))
        .unwrap_or_else(|_| [(); 64].map(|_| rand::thread_rng().gen()));
    let session_layer = SessionLayer::new(store, &secret).with_secure(false);

    let mut scheduler = Scheduler::new();
    scheduler.every(15.minutes()).run(move || {
        println!("[!] clearing db...");
        db::reset();
    });
    let _thread_handle = scheduler.watch_thread(std::time::Duration::from_millis(100));

    let tera = match Tera::new("templates/**/*.html") {
        Ok(t) => t,
        Err(e) => {
            println!("Parsing error(s): {}", e);
            ::std::process::exit(1);
        }
    };

    let app = Router::new()
        .nest_service("/public", ServeDir::new("public"))
        .nest("/admin/", routes::admin::router())
        .nest("/space/", routes::space::router())
        .nest("/api/", routes::api::router())
        .nest("/", routes::root::router())
        .layer(session_layer)
        .layer(Extension(tera))
        .layer(middleware::from_fn(utils::security));

    let port: u16 = option_env!("PORT")
        .and_then(|p| p.parse().ok())
        .unwrap_or(1337);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("crabspace listening on http://localhost:{}", port);

    db::reset();

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

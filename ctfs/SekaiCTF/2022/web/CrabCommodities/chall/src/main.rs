use actix_session::{storage::CookieSessionStore, SessionMiddleware};
use actix_web::cookie::Key;
use actix_web::{error, get, web, App, Error, HttpResponse, HttpServer};
use clokwerk::{Scheduler, TimeUnits};
use dashmap::DashMap;
use num_format::{Locale, ToFormattedString};
use once_cell::sync::Lazy;
use std::collections::HashMap;
use tera::{Context, Tera, Value};
use include_dir::{include_dir, Dir};

static TEMPLATE_DIR: Dir = include_dir!("$CARGO_MANIFEST_DIR/src/templates");

mod api;
mod auth;
mod game;

pub static USERS: Lazy<DashMap<String, game::User>> = Lazy::new(DashMap::new);

#[get("/")]
async fn index(tera: web::Data<Tera>) -> Result<HttpResponse, Error> {
    match tera.render("index.html", &Context::new()) {
        Ok(body) => Ok(HttpResponse::Ok().body(body)),
        Err(err) => Err(error::ErrorInternalServerError(err)),
    }
}

#[get("/login")]
pub async fn login(tera: web::Data<Tera>) -> Result<HttpResponse, Error> {
    match tera.render("login.html", &Context::new()) {
        Ok(body) => Ok(HttpResponse::Ok().body(body)),
        Err(err) => Err(error::ErrorInternalServerError(err)),
    }
}

#[get("/register")]
pub async fn register(tera: web::Data<Tera>) -> Result<HttpResponse, Error> {
    match tera.render("register.html", &Context::new()) {
        Ok(body) => Ok(HttpResponse::Ok().body(body)),
        Err(err) => Err(error::ErrorInternalServerError(err)),
    }
}

// tera extra display filters
pub fn to_money(value: &Value, _: &HashMap<String, Value>) -> Result<Value, tera::Error> {
    let s: i64 = tera::try_get_value!("to_money", "value", i64, value);
    Ok(Value::String(format!(
        "${}",
        s.to_formatted_string(&Locale::en)
    )))
}
pub fn to_money_negative(value: &Value, _: &HashMap<String, Value>) -> Result<Value, tera::Error> {
    let s: i64 = tera::try_get_value!("to_money_negative", "value", i64, value);
    Ok(Value::String(format!(
        "${}",
        (-s).to_formatted_string(&Locale::en)
    )))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port: u16 = std::env::var("PORT")
        .unwrap_or_else(|_| "1337".to_string())
        .parse()
        .expect("Invalid PORT variable");
    let secret_key = Key::generate();

    let mut scheduler = Scheduler::new();
    scheduler.every(10.minutes()).run(|| {
        println!("[!] clearing users DB");
        USERS.clear();
    });
    let _thread_handle = scheduler.watch_thread(std::time::Duration::from_millis(100));

    println!("Listening on 0.0.0.0:{}", port);

    HttpServer::new(move || {
        let mut tera = Tera::default();
        for entry in TEMPLATE_DIR.find("**/*.html").unwrap() {
            if let Some(file) = entry.as_file() {
                if let (Some(path), Some(contents)) = (file.path().to_str(), file.contents_utf8()) {
                    if tera.add_raw_template(path, contents).is_err() {
                        println!("[!] Error reading template {}", path);
                    }
                }
            }
        }

        tera.register_filter("to_money", to_money);
        tera.register_filter("to_money_negative", to_money_negative);

        let cookie_session =
            SessionMiddleware::builder(CookieSessionStore::default(), secret_key.clone())
                .cookie_secure(false)
                .build();

        App::new()
            .app_data(web::Data::new(tera))
            .wrap(cookie_session)
            .service(auth::routes())
            .service(api::routes())
            .service(game::game_route)
            .service(login)
            .service(register)
            .service(index)
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await
}

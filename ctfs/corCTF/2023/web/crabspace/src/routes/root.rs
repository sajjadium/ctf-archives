use crate::utils;
use crate::utils::Context;
use axum::{response::Html, routing::get, Extension, Router};
use tera::Tera;

async fn login(Extension(tera): Extension<Tera>, ctx: Context) -> Html<String> {
    utils::render(tera, "login.html", ctx.tera)
}

async fn register(Extension(tera): Extension<Tera>, ctx: Context) -> Html<String> {
    utils::render(tera, "register.html", ctx.tera)
}

async fn index(Extension(tera): Extension<Tera>, ctx: Context) -> Html<String> {
    match ctx.user {
        Some(_) => utils::render(tera, "home.html", ctx.tera),
        None => utils::render(tera, "index.html", ctx.tera),
    }
}

pub fn router() -> Router {
    Router::new()
        .route("/login", get(login))
        .route("/register", get(register))
        .route("/", get(index))
}

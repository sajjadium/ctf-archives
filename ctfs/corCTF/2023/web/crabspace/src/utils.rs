use async_trait::async_trait;
use axum::{
    extract::FromRequestParts,
    http::{header::InvalidHeaderValue, request::Parts, HeaderValue, Request, StatusCode},
    middleware::Next,
    response::{Html, IntoResponse, Redirect, Response},
    Extension,
};
use axum_sessions::{async_session::Session, SessionHandle};
use tera::Tera;
use tokio::sync::OwnedRwLockWriteGuard;
use uuid::Uuid;

use crate::db::{User, USERS};

/* Wrapper over Tera context & session */
pub struct Context {
    pub tera: tera::Context,
    pub sess: OwnedRwLockWriteGuard<Session>,
    pub user: Option<User>,
}

#[async_trait]
impl<S> FromRequestParts<S> for Context
where
    S: Send + Sync,
{
    type Rejection = Redirect;

    async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let Extension(session_handle): Extension<SessionHandle> =
            Extension::from_request_parts(parts, state)
                .await
                .expect("Session extension missing. Is the session layer installed?");
        let mut sess = session_handle.write_owned().await;
        let mut tera = tera::Context::new();

        if let Some(err) = sess.get::<String>("error") {
            sess.remove("error");
            tera.insert("error", &err);
        }
        if let Some(info) = sess.get::<String>("info") {
            sess.remove("info");
            tera.insert("info", &info);
        }

        let mut user: Option<User> = None;
        if let Some(id) = sess.get::<Uuid>("id") {
            user = USERS.get(&id).map(|v| User {
                pass: "".to_string(),
                ..v.clone()
            });
            tera.insert("user", &user);
        }

        Ok(Context { tera, sess, user })
    }
}

pub async fn security<B>(req: Request<B>, next: Next<B>) -> AppResult<Response> {
    let mut res = next.run(req).await;
    let headers = res.headers_mut();
    headers.insert(
        "Content-Security-Policy",
        HeaderValue::try_from(
            [
                "default-src 'none'",
                "style-src 'self'",
                "script-src 'unsafe-inline'",
                "frame-ancestors 'none'",
            ]
            .join("; "),
        )?,
    );
    headers.insert(
        "Cross-Origin-Opener-Policy",
        HeaderValue::from_static("same-origin"),
    );
    headers.insert("X-Frame-Options", HeaderValue::from_static("DENY"));
    headers.insert("Cache-Control", HeaderValue::from_static("no-cache, no-store"));
    Ok(res)
}

pub fn render(tera: Tera, template: &str, ctx: tera::Context) -> Html<String> {
    Html(match tera.render(template, &ctx) {
        Ok(r) => r,
        Err(e) => e.to_string(),
    })
}

pub struct AppError(&'static str);
pub type AppResult<T> = Result<T, AppError>;
impl From<axum_sessions::async_session::serde_json::Error> for AppError {
    fn from(_value: axum_sessions::async_session::serde_json::Error) -> Self {
        AppError("An internal server error occurred")
    }
}
impl From<tera::Error> for AppError {
    fn from(_value: tera::Error) -> Self {
        AppError("An internal server error occurred")
    }
}
impl From<InvalidHeaderValue> for AppError {
    fn from(_value: InvalidHeaderValue) -> Self {
        AppError("An internal server error occurred")
    }
}
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Something went wrong: {}", self.0),
        )
            .into_response()
    }
}

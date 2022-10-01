use actix_session::{Session, SessionExt};
use actix_web::{error, post, web, Either, FromRequest, HttpRequest, HttpResponse, Scope};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::future::{ready, Ready};

use crate::{game::User, USERS};

// hint: you can skip understanding this file, there are no vulnerabilities
// (at least, i think)

impl FromRequest for User {
    type Error = <Session as FromRequest>::Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, _payload: &mut actix_web::dev::Payload) -> Self::Future {
        let session = req.get_session();

        let session_data = match session.get("username") {
            Ok(session_data) => session_data,
            Err(_) => {
                return ready(Err(error::ErrorUnauthorized(
                    r#"{"success": false, "error": "You are not logged in"}"#,
                )))
            }
        };

        let username: String = match session_data {
            Some(username) => username,
            None => {
                return ready(Err(error::ErrorUnauthorized(
                    r#"{"success": false, "error": "You are not logged in"}"#,
                )))
            }
        };

        let user = match USERS.get(&username) {
            Some(user) => user,
            None => {
                return ready(Err(error::ErrorUnauthorized(
                    r#"{"success": false, "error": "You are not logged in"}"#,
                )))
            }
        };

        ready(Ok(user.to_owned()))
    }
}

pub fn sha256(input: &str) -> String {
    format!("{:x}", Sha256::digest(input))
}

#[derive(Deserialize)]
struct AuthPayload {
    username: String,
    password: String,
}

#[post("/login")]
async fn login(
    session: Session,
    body: web::Form<AuthPayload>,
) -> Either<&'static str, HttpResponse> {
    let user = match USERS.get(&body.username) {
        Some(user) => user,
        None => return Either::Left("No user exists with that username"),
    };

    let hash = sha256(&body.password);

    if user.password != hash {
        return Either::Left("Invalid password");
    }

    if session.insert("username", &body.username).is_err() {
        return Either::Left("There was an error setting your user");
    }

    Either::Right(
        HttpResponse::Found()
            .append_header(("Location", "/game"))
            .finish(),
    )
}

#[post("/register")]
async fn register(
    session: Session,
    body: web::Form<AuthPayload>,
) -> Either<&'static str, HttpResponse> {
    if body.password.len() < 8 {
        return Either::Left("Please choose a longer password");
    }

    if USERS.contains_key(&body.username) {
        return Either::Left("A user already exists with that username");
    }

    let hash = sha256(&body.password);
    let user = User::new(body.username.clone(), hash);

    USERS.insert(body.username.clone(), user);
    if session.insert("username", &body.username).is_err() {
        return Either::Left("There was an error setting your user");
    }

    Either::Right(
        HttpResponse::Found()
            .append_header(("Location", "/game"))
            .finish(),
    )
}

pub fn routes() -> Scope {
    web::scope("/auth").service(register).service(login)
}

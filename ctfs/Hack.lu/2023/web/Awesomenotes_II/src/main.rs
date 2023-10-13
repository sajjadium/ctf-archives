pub mod math_tags;

use axum::{
    extract::Multipart,
    extract::Path,
    headers::Cookie,
    http::{header::LOCATION, HeaderMap, HeaderValue, StatusCode},
    response::Html,
    routing::{get, post},
    Form, Router, TypedHeader,
};
use math_tags::TAGS;
use serde::Deserialize;
use std::{fs, io::Read};
use tower_http::services::ServeDir;

#[derive(Deserialize)]
struct Report {
    link: String,
    #[serde(rename = "g-recaptcha-response")]
    captcha: String,
}

#[tokio::main]
async fn main() {
    // build our application with a single route
    let app = Router::new()
        .route("/", get(home))
        .route("/create", get(create))
        .route("/report", get(report))
        .route("/note/:note", get(note))
        .route("/api/report", post(take_report))
        .route("/api/note/:note", get(get_note))
        .route("/api/note", post(upload_note))
        .nest_service("/static", ServeDir::new("public/static"));
    // run it with hyper on localhost:3000
    let server =
        axum::Server::bind(&"0.0.0.0:3000".parse().unwrap()).serve(app.into_make_service());
    println!("🚀 App running on 0.0.0.0:3000 🚀");
    server.await.unwrap();
}

// which calls one of these handlers
async fn home() -> Html<String> {
    Html(fs::read_to_string("public/index.html").expect("Missing html files"))
}

async fn report() -> Html<String> {
    Html(fs::read_to_string("public/report.html").expect("Missing html files"))
}

async fn create() -> Html<String> {
    Html(fs::read_to_string("public/create.html").expect("Missing html files"))
}

async fn note() -> Html<String> {
    Html(fs::read_to_string("public/note.html").expect("Missing html files"))
}

//API
async fn get_note(
    Path(note): Path<String>,
    TypedHeader(cookie): TypedHeader<Cookie>,
) -> Result<Html<String>, (StatusCode, &'static str)> {
    if &note == "flag" {
        let Some(name) = cookie.get("session") else {
            return Err((StatusCode::UNAUTHORIZED, "Missing session cookie"));
        };
        if name != std::env::var("ADMIN_SESSION").expect("Missing ADMIN_SESSION") {
            return Err((
                StatusCode::UNAUTHORIZED,
                "You are not allowed to read this note",
            ));
        }
        return Ok(Html(fs::read_to_string("flag.txt").expect("Flag missing")));
    }
    if note.chars().any(|c| !c.is_ascii_hexdigit()) {
        return Err((StatusCode::BAD_REQUEST, "Malformed note ID"));
    }
    let Ok(note) = fs::read_to_string(format!("public/upload/{:}", note)) else {
        return Err((StatusCode::NOT_FOUND, "Note not found"));
    };
    Ok(Html(note))
}

async fn upload_note(
    mut multipart: Multipart,
) -> (StatusCode, Result<HeaderMap<HeaderValue>, &'static str>) {
    let mut body: Option<String> = None;
    while let Some(field) = multipart.next_field().await.unwrap() {
        let Some(name) = field.name() else { continue };
        if name != "note" {
            continue;
        }
        let Ok(data) = field.text().await else {
            continue;
        };
        body = Some(data);
        break;
    }
    let Some(body) = body else {
        return (StatusCode::BAD_REQUEST, Err("Malformed formdata"));
    };
    if body.len() > 5000 {
        return (StatusCode::PAYLOAD_TOO_LARGE, Err("Note too big"));
    }
    let safe = ammonia::Builder::new()
        .add_tags(TAGS)
        .add_tags(&["style"])
        .rm_clean_content_tags(&["style"])
        /*
            Thank god we don't have any more XSS vulnerabilities now 🙏
        */
        // .add_generic_attribute_prefixes(&["hx-"])
        .clean(&body)
        .to_string();
    let mut name = [0u8; 32];
    fs::File::open("/dev/urandom")
        .unwrap()
        .read_exact(&mut name)
        .expect("Failed to read urandom");
    let name = String::from_iter(name.map(|c| format!("{:02x}", c)));
    fs::write(format!("public/upload/{:}", name), safe).expect("Failed to write note");
    (
        StatusCode::FOUND,
        Ok(HeaderMap::from_iter([(
            LOCATION,
            format!("/note/{:}", name).parse().unwrap(),
        )])),
    )
}

async fn take_report(Form(report): Form<Report>) -> Result<String, (StatusCode, &'static str)> {
    let params = [("link", report.link), ("recaptcha", report.captcha)];
    let client = reqwest::Client::new();
    let res = client
        .post(format!(
            "http://{:}",
            std::env::var("BOT_HOST").expect("Missing BOT_HOST")
        ))
        .form(&params)
        .send()
        .await
        .expect("Can't request bot");
    if res.status() != StatusCode::OK {
        return Err((StatusCode::BAD_REQUEST, "Report failed"));
    }
    Ok(
        std::fs::read_to_string("public/static/fragment/report_success.html")
            .expect("Missing fragment"),
    )
}

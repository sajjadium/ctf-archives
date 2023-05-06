mod ast_validator;
mod code_generator;

use actix_web::Responder;
use actix_web::{error, web, HttpRequest, HttpResponse, HttpServer};
use rand::Rng;
use serde::{Deserialize, Serialize};
use std::path;

fn get_user_id() -> String {
    rand::thread_rng()
        .sample_iter(rand::distributions::Alphanumeric)
        .take(16)
        .map(char::from)
        .collect()
}

fn validate_user_id(id: &str) -> actix_web::Result<&str> {
    if id.len() == 16 && id.chars().all(|c| c.is_ascii_alphanumeric()) {
        Ok(id)
    } else {
        Err(error::ErrorBadRequest("Invalid id"))
    }
}

fn validate_filename(filename: &str) -> actix_web::Result<&str> {
    if filename.ends_with(".json")
        && filename
            .chars()
            .rev()
            .skip(".json".len())
            .all(|c| c.is_ascii_alphanumeric())
    {
        Ok(filename)
    } else {
        Err(error::ErrorBadRequest("Invalid filename"))
    }
}

#[actix_web::get("/")]
async fn index() -> actix_web::Result<actix_files::NamedFile> {
    let file = actix_files::NamedFile::open("views/index.html")?;
    Ok(file)
}

#[derive(Deserialize)]
struct ProgramData {
    source: String,
}

#[actix_web::post("/")]
async fn create_program(req_body: web::Json<ProgramData>) -> actix_web::Result<impl Responder> {
    let source = req_body.source.as_str();
    if source.len() > 300 {
        Err(error::ErrorBadRequest("Too long program"))?;
    }
    if !source.is_ascii() {
        Err(error::ErrorBadRequest("Invalid characters"))?;
    }

    let source = ast_validator::validate(source).map_err(error::ErrorBadRequest)?;

    let user_id = get_user_id();
    let user_path = code_generator::generate(source, &user_id)
        .map_err(|_| error::ErrorInternalServerError(""))?;

    Ok(HttpResponse::Ok().body(format!("/{}", user_path)))
}

#[actix_web::get("/sandbox/{id}")]
async fn sandbox_index(req: HttpRequest) -> actix_web::Result<actix_files::NamedFile> {
    let _ = validate_user_id(req.match_info().get("id").unwrap())?;
    let file = actix_files::NamedFile::open("views/sandbox.html")?;
    Ok(file)
}

#[actix_web::get("/sandbox/{id}/preview")]
async fn sandbox_preview(req: HttpRequest) -> actix_web::Result<actix_files::NamedFile> {
    let id = validate_user_id(req.match_info().get("id").unwrap())?;
    let preview_path = path::Path::new("sandbox").join(id).join("preview.ts");
    let file = actix_files::NamedFile::open(preview_path)?;
    Ok(file)
}

#[derive(Deserialize)]
struct RunRequestData {
    input: String,
}

#[derive(Serialize)]
struct RunResponseData {
    filename: Option<String>,
    error_msg: Option<String>,
}

#[actix_web::post("/sandbox/{id}/run")]
async fn sandbox_run(
    req: HttpRequest,
    req_body: web::Json<RunRequestData>,
) -> actix_web::Result<impl Responder> {
    let id = validate_user_id(req.match_info().get("id").unwrap())?;

    let sandbox_path = path::Path::new("sandbox").join(id);
    let output = async_process::Command::new("timeout")
        .args([
            "5s",
            "deno",
            "run",
            "--allow-write=.",
            "main.ts",
            &req_body.input,
        ])
        .current_dir(&sandbox_path)
        .stdout(async_process::Stdio::piped())
        .stderr(async_process::Stdio::piped())
        .output()
        .await?;

    let code = output.status.code().unwrap_or(1);
    let stdout = String::from_utf8(output.stdout).unwrap_or_default();
    let stderr = String::from(if code == 124 {
        "Timeout"
    } else {
        "Something wrong"
    });

    Ok(web::Json(RunResponseData {
        filename: (code == 0).then_some(stdout),
        error_msg: (code != 0).then_some(stderr),
    }))
}

#[actix_web::get("/sandbox/{id}/show/{filename}")]
async fn sandbox_show(req: HttpRequest) -> actix_web::Result<actix_files::NamedFile> {
    let id = validate_user_id(req.match_info().get("id").unwrap())?;
    let filename = validate_filename(req.match_info().get("filename").unwrap())?;
    let file_path = path::Path::new("sandbox").join(id).join(filename);
    let file = actix_files::NamedFile::open(file_path)?;
    Ok(file)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();

    HttpServer::new(|| {
        actix_web::App::new()
            .wrap(actix_web::middleware::Logger::default())
            .service(index)
            .service(create_program)
            .service(sandbox_index)
            .service(sandbox_preview)
            .service(sandbox_run)
            .service(sandbox_show)
    })
    .bind(("0.0.0.0", 3000))?
    .run()
    .await
}

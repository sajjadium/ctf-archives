use crate::handler::helper::HandlerResult;
use crate::process_image::process_image;
use anyhow::Context;
use axum::debug_handler;
use axum::extract;
use axum::http::StatusCode;
use axum::response::IntoResponse;
use bytes::Bytes;
use std::path::PathBuf;
use tokio::fs;
use uuid::Uuid;

// POST /create
#[debug_handler]
pub async fn handle_create(mut multipart: extract::Multipart) -> HandlerResult {
    let id = Uuid::new_v4();

    let current_dir = PathBuf::from(format!("./data/{id}"));
    fs::create_dir(&current_dir)
        .await
        .context("Failed to create working directory")?;

    let (file_name, file_data) = match extract_file(&mut multipart).await {
        Some(file) => file,
        None => return Ok((StatusCode::BAD_REQUEST, "Invalid multipart data").into_response()),
    };
    fs::write(
        current_dir.join(file_name.file_name().unwrap_or("".as_ref())),
        file_data,
    )
    .await
    .context("Failed to save uploaded file")?;

    process_image(&current_dir, &file_name)
        .await
        .context("Failed to process image")?;

    Ok((StatusCode::SEE_OTHER, [("location", format!("/view/{id}"))]).into_response())
}

// Extract file name and file data from multipart form data
async fn extract_file(multipart: &mut extract::Multipart) -> Option<(PathBuf, Bytes)> {
    while let Ok(Some(field)) = multipart.next_field().await {
        if field.name() == Some("file") {
            let file_name = match field.file_name() {
                Some(file_name) => PathBuf::from(file_name),
                None => return None,
            };
            let file_data = match field.bytes().await {
                Ok(bytes) => bytes,
                Err(_) => return None,
            };

            return Some((file_name, file_data));
        }
    }

    None
}

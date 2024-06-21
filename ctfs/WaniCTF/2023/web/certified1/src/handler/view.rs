use crate::handler::helper::HandlerResult;
use anyhow::Context;
use axum::debug_handler;
use axum::extract;
use axum::response::IntoResponse;
use tokio::fs;
use uuid::Uuid;

// GET /view
#[debug_handler]
pub async fn handle_view(
    extract::Path(id): extract::Path<Uuid>,
) -> HandlerResult<impl IntoResponse> {
    let data = fs::read(format!("./data/{id}/output.png"))
        .await
        .context("Failed to read file")?;

    Ok(([("content-type", "image/png")], data))
}

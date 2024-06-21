use axum::debug_handler;
use axum::response::Html;

// GET /
#[debug_handler]
pub async fn handle_index() -> Html<&'static str> {
    Html(include_str!("../../assets/index.html"))
}

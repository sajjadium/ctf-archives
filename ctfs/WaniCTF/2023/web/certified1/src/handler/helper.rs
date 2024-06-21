use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};

pub type HandlerResult<T = Response> = std::result::Result<T, HandlerError>;

pub struct HandlerError {
    err: anyhow::Error,
}

impl From<anyhow::Error> for HandlerError {
    fn from(err: anyhow::Error) -> Self {
        Self { err }
    }
}

impl IntoResponse for HandlerError {
    fn into_response(self) -> Response {
        (StatusCode::INTERNAL_SERVER_ERROR, format!("{:?}", self.err)).into_response()
    }
}

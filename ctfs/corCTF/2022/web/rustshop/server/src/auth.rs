use axum::{
    async_trait,
    extract::{FromRequest, RequestParts},
    http::StatusCode,
    Json,
};
use tower_cookies::Cookies;

use crate::utils::{APIResponse, APIStatus, User, DB, SESSIONS};

#[async_trait]
impl<B> FromRequest<B> for User
where
    B: Send,
{
    type Rejection = (StatusCode, axum::Json<APIResponse>);

    async fn from_request(req: &mut RequestParts<B>) -> Result<Self, Self::Rejection> {
        let extensions = req.extensions_mut();
        let cookies: &Cookies = extensions.get().expect("Cookie extension missing");

        let session_cookie = cookies.get("session");

        let session_cookie = match session_cookie {
            Some(session_cookie) => session_cookie.value().to_string(),
            _ => {
                return Err((
                    StatusCode::OK,
                    Json(APIResponse {
                        status: APIStatus::Error,
                        data: None,
                        message: Some(String::from("Missing session cookie")),
                    }),
                ));
            }
        };

        let username = match SESSIONS.get(&session_cookie) {
            Some(username) => username,
            _ => {
                return Err((
                    StatusCode::OK,
                    Json(APIResponse {
                        status: APIStatus::Error,
                        data: None,
                        message: Some(String::from("Invalid session cookie")),
                    }),
                ));
            }
        };

        let user = match DB.get(&username.to_string()) {
            Some(user) => user,
            _ => {
                return Err((
                    StatusCode::OK,
                    Json(APIResponse {
                        status: APIStatus::Error,
                        data: None,
                        message: Some(String::from("Invalid session cookie")),
                    }),
                ));
            }
        };

        Ok(user.clone())
    }
}

use axum::{
    extract::Path,
    response::{IntoResponse, Redirect, Response},
    routing::get,
    Extension, Router,
};
use tera::Tera;
use uuid::Uuid;

use crate::utils;
use crate::{
    db::USERS,
    utils::{AppResult, Context},
};

async fn space(
    Extension(tera): Extension<Tera>,
    Path(id): Path<Uuid>,
    mut ctx: Context,
) -> AppResult<Response> {
    Ok(match USERS.get(&id) {
        Some(user) => {
            ctx.tera.insert(
                "space",
                &Tera::one_off(&user.space, &ctx.tera, true).unwrap_or_else(|_| user.space.clone()),
            );
            ctx.tera.insert("id", &id);
            utils::render(tera, "space.html", ctx.tera).into_response()
        }
        None => {
            ctx.sess
                .insert("error", "Could not find the space for that user")?;
            Redirect::to("/").into_response()
        }
    })
}

pub fn router() -> Router {
    Router::new().route("/:id", get(space))
}

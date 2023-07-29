use crate::utils;
use crate::{
    db::{User, USERS},
    utils::{AppResult, Context},
};
use axum::extract::Query;
use axum::{
    extract::Path,
    response::{IntoResponse, Redirect, Response},
    routing::get,
    Extension, Router,
};
use serde::{Deserialize, Serialize};
use tera::Tera;
use uuid::Uuid;

#[derive(Serialize)]
struct UserView {
    id: Uuid,
    name: String,
    following: Vec<User>,
    followers: Vec<User>,
    space: String,
}

#[derive(Deserialize)]
struct AdminQuery {
    sort: Option<String>,
}

impl From<User> for UserView {
    fn from(u: User) -> Self {
        UserView {
            id: u.id,
            name: u.name,
            following: u
                .following
                .iter()
                .filter_map(|f| USERS.get(f).map(|f| f.clone()))
                .collect(),
            followers: u
                .followers
                .iter()
                .filter_map(|f| USERS.get(f).map(|f| f.clone()))
                .collect(),
            space: u.space,
        }
    }
}

async fn admin(
    Extension(tera): Extension<Tera>,
    Path(id): Path<Uuid>,
    Query(query): Query<AdminQuery>,
    mut ctx: Context,
) -> AppResult<Response> {
    let Some(user) = ctx.user else {
        ctx.sess.insert("error", "Permission denied")?;
        return Ok(Redirect::to("/").into_response());
    };

    if user.name != "admin" {
        ctx.sess.insert("error", "Permission denied")?;
        return Ok(Redirect::to("/").into_response());
    }

    let Some(target) = USERS.get(&id) else {
        ctx.sess.insert("error", "Could not find that user")?;
        return Ok(Redirect::to("/").into_response());
    };

    if target.name == "admin" {
        ctx.sess.insert("error", "Give the admin some privacy...")?;
        return Ok(Redirect::to("/").into_response());
    }

    let target: UserView = target.clone().into();

    ctx.tera.insert("target", &target);
    ctx.tera
        .insert("sort", &query.sort.unwrap_or_else(|| "id".to_string()));
    Ok(utils::render(tera, "admin.html", ctx.tera).into_response())
}

pub fn router() -> Router {
    Router::new().route("/:id", get(admin))
}

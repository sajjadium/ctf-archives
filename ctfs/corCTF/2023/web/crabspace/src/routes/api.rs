use axum::http::Request;
use axum::middleware::{self, Next};
use axum::response::{IntoResponse, Response};
use axum::{response::Redirect, routing::post, Form, Router};
use serde::Deserialize;
use uuid::Uuid;

use crate::db::{User, NAMES, USERS};
use crate::utils::{AppResult, Context};

#[derive(Deserialize)]
struct UserPayload {
    name: String,
    pass: String,
}

async fn register(mut ctx: Context, Form(body): Form<UserPayload>) -> AppResult<Redirect> {
    if NAMES.contains_key(&body.name) {
        ctx.sess
            .insert("error", "A user already exists with that username")?;
        return Ok(Redirect::to("/register"));
    }

    if body.name.len() < 5 || body.pass.len() < 7 {
        ctx.sess
            .insert("error", "Username or password is too short")?;
        return Ok(Redirect::to("/register"));
    }

    let id = Uuid::new_v4();
    let user = User {
        id,
        name: body.name.to_string(),
        pass: body.pass,
        followers: vec![],
        following: vec![],
        space: format!("Welcome to <b>{}</b>'s space!", body.name),
    };

    ctx.sess.insert("info", "Registered successfully")?;
    ctx.sess.insert("id", id)?;
    USERS.insert(user.id, user);
    NAMES.insert(body.name, id);
    Ok(Redirect::to("/"))
}

async fn login(mut ctx: Context, Form(body): Form<UserPayload>) -> AppResult<Redirect> {
    let Some(id) = NAMES.get(&body.name) else {
        ctx.sess.insert("error", "No user exists with that username")?;
        return Ok(Redirect::to("/login"));
    };

    let Some(user) = USERS.get(&id) else {
        ctx.sess.insert("error", "No user exists with that username")?;
        return Ok(Redirect::to("/login"));
    };

    if user.pass != body.pass {
        ctx.sess.insert("error", "Incorrect password")?;
        return Ok(Redirect::to("/login"));
    }

    ctx.sess.insert("info", "Logged in successfully")?;
    ctx.sess.insert("id", user.id)?;
    Ok(Redirect::to("/"))
}

async fn requires_auth<B>(
    mut ctx: Context,
    request: Request<B>,
    next: Next<B>,
) -> AppResult<Response> {
    let Some(user) = &ctx.user else {
        ctx.sess.insert("error", "You must be logged in")?;
        return Ok(Redirect::to("/login").into_response());
    };

    if user.name == "admin" {
        ctx.sess.insert("error", "This action is currently disabled for admins.")?;
        return Ok(Redirect::to("/").into_response());
    }

    drop(ctx); // required to not deadlock :>
    Ok(next.run(request).await.into_response())
}

#[derive(Deserialize)]
struct SpacePayload {
    space: String,
}
async fn space(mut ctx: Context, Form(body): Form<SpacePayload>) -> AppResult<Redirect> {
    if body.space.len() > 200 {
        ctx.sess.insert("error", "Sorry, your space is too long.")?;
        return Ok(Redirect::to("/"));
    }

    let id = ctx.user.unwrap().id;
    let user = USERS.get(&id).unwrap().clone();

    USERS.insert(
        id,
        User {
            space: body.space,
            ..user
        },
    );

    ctx.sess.insert("info", "Updated your space")?;
    Ok(Redirect::to("/"))
}

#[derive(Deserialize)]
struct FollowPayload {
    id: Uuid,
}
async fn follow(mut ctx: Context, Form(body): Form<FollowPayload>) -> AppResult<Redirect> {
    let id = ctx.user.unwrap().id;

    let mut user = USERS.get_mut(&id).unwrap();
    let following = &mut user.following;
    if following.contains(&body.id) {
        ctx.sess.insert("info", "Unfollowed")?;
        following.retain(|x| *x != body.id);
    } else {
        ctx.sess.insert("info", "Followed")?;
        following.push(body.id);
    }
    drop(user);

    let Some(mut target) = USERS.get_mut(&body.id) else {
        ctx.sess.insert("error", "No user found with that id")?;
        return Ok(Redirect::to("/"));
    };
    let followers = &mut target.followers;
    if followers.contains(&id) {
        followers.retain(|x| *x != id);
    } else {
        followers.push(id);
    }

    Ok(Redirect::to(format!("/space/{}", body.id).as_str()))
}

pub fn router() -> Router {
    Router::new()
        .route("/follow", post(follow))
        .route("/space", post(space))
        .route_layer(middleware::from_fn(requires_auth))
        .route("/register", post(register))
        .route("/login", post(login))
}

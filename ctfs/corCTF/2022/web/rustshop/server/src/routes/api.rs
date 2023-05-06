use crate::utils;
use crate::utils::{APIResponse, APIStatus, PurchasedItem, ShopItem, User, DB, SESSIONS};
use axum::{
    routing::{get, post},
    Json, Router,
};
use once_cell::sync::Lazy;
use serde_json::json;
use std::env;
use tower_cookies::{Cookie, Cookies};

static ITEMS: Lazy<&'static [ShopItem]> = Lazy::new(|| {
    &[
        ShopItem {
            name: "Ferris Plush",
            image: "https://cdn.shopify.com/s/files/1/0154/2777/products/4_1024x1024.jpg",
            price: 100,
        },
        ShopItem {
            name: "Programming Socks",
            image: "https://m.media-amazon.com/images/I/61VyCXfaRXL._AC_UL320_.jpg",
            price: 500,
        },
        //      ShopItem {
        //          name: "rustshop flag",
        //          image: "https://ctf.cor.team/assets/img/ctflogo.png",
        //          price: 13371337
        //      }
    ]
});

async fn user_get(user: User) -> Json<APIResponse> {
    Json(APIResponse {
        status: APIStatus::Success,
        data: Some(json!(user)),
        message: None,
    })
}

async fn register_post(Json(body): Json<serde_json::Value>, cookies: Cookies) -> Json<APIResponse> {
    if !utils::validate_body(&body, &["username", "password"]) {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("Invalid input")),
        });
    }

    let mut user: User = match serde_json::from_value(body) {
        Ok(user) => user,
        Err(_) => {
            return Json(APIResponse {
                status: APIStatus::Error,
                data: None,
                message: Some(String::from("Missing username or password")),
            })
        }
    };

    if user.username.len() < 5 || user.password.len() < 7 {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("Username or password too short")),
        });
    }

    if DB.contains_key(&user.username) {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("A user already exists with that username")),
        });
    }

    user.password = utils::sha256(user.password);

    let username = user.username.to_string();
    let session_cookie = utils::randstr(64);

    SESSIONS.insert(session_cookie.to_string(), username.to_string());
    cookies.add(Cookie::new("session", session_cookie));
    DB.insert(username, user);

    Json(APIResponse {
        status: APIStatus::Success,
        data: None,
        message: None,
    })
}

async fn login_post(Json(body): Json<serde_json::Value>, cookies: Cookies) -> Json<APIResponse> {
    if !utils::validate_body(&body, &["username", "password"]) {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("Invalid input")),
        });
    }

    let body: User = match serde_json::from_value(body) {
        Ok(user) => user,
        Err(_) => {
            return Json(APIResponse {
                status: APIStatus::Error,
                data: None,
                message: Some(String::from("Missing username or password")),
            })
        }
    };

    let user = match DB.get(&body.username) {
        None => {
            return Json(APIResponse {
                status: APIStatus::Error,
                data: None,
                message: Some(String::from("Incorrect username or password")),
            })
        }
        Some(user) => user,
    };

    if user.password != utils::sha256(body.password) {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("Incorrect username or password")),
        });
    }

    let session_cookie = utils::randstr(64);
    SESSIONS.insert(session_cookie.to_string(), body.username.to_string());
    cookies.add(Cookie::new("session", session_cookie));

    Json(APIResponse {
        status: APIStatus::Success,
        data: None,
        message: None,
    })
}

async fn items_get() -> Json<APIResponse> {
    Json(APIResponse {
        status: APIStatus::Success,
        data: Some(json!(Lazy::force(&ITEMS))),
        message: None,
    })
}

async fn buy_post(user: User, Json(body): Json<serde_json::Value>) -> Json<APIResponse> {
    if !utils::validate_body(&body, &["name", "quantity"]) {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("Invalid input")),
        });
    }

    let body: PurchasedItem = match serde_json::from_value(body) {
        Ok(user) => user,
        Err(_) => {
            return Json(APIResponse {
                status: APIStatus::Error,
                data: None,
                message: Some(String::from("Missing name or quantity")),
            })
        }
    };

    let item: &ShopItem = match ITEMS.iter().find(|i| i.name == body.name) {
        Some(item) => item,
        None => {
            return Json(APIResponse {
                status: APIStatus::Error,
                data: None,
                message: Some(String::from("No shop item exists with that name")),
            })
        }
    };

    if body.quantity <= 0 {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("You can only buy a positive quantity")),
        });
    }

    if body.quantity > 100 {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("You can buy max 100 items at a time")),
        });
    }

    let price = item.price * body.quantity;
    if user.money < price {
        return Json(APIResponse {
            status: APIStatus::Error,
            data: None,
            message: Some(String::from("You don't have enough money to buy that")),
        });
    }

    let mut new_user = user.clone();
    new_user.money -= price;
    match new_user.items.iter_mut().find(|i| i.name == body.name) {
        Some(user_item) => user_item.quantity += body.quantity,
        None => new_user.items.push(body),
    };

    DB.insert(user.username, new_user);

    Json(APIResponse {
        status: APIStatus::Success,
        data: None,
        message: None,
    })
}

async fn flag_get(user: User) -> Json<APIResponse> {
    if user.money == 0x13371337 {
        for item in user.items {
            if item.name == "rustshop flag" && item.quantity == 0x42069 {
                return Json(APIResponse {
                    status: APIStatus::Success,
                    data: None,
                    message: Some(
                        env::var("FLAG").unwrap_or_else(|_| "flag{test_flag}".to_string()),
                    ),
                });
            }
        }
    }
    Json(APIResponse {
        status: APIStatus::Error,
        data: None,
        message: Some("no shot".to_string()),
    })
}

pub fn router() -> Router {
    Router::new()
        .route("/user", get(user_get))
        .route("/register", post(register_post))
        .route("/login", post(login_post))
        .route("/items", get(items_get))
        .route("/buy", post(buy_post))
        .route("/flag", get(flag_get))
}

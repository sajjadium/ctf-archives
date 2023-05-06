use actix_web::{
    post,
    web::{self, Json},
    Scope,
};
use serde::{Deserialize, Serialize};

use crate::game::{Game, InventoryItem, User};

#[derive(Serialize)]
struct APIResult {
    success: bool,
    message: &'static str,
}

#[derive(Deserialize)]
struct ItemPayload {
    name: String,
    quantity: i32,
}

#[post("/buy")]
async fn buy(user: User, body: web::Form<ItemPayload>) -> Json<APIResult> {
    if user.game.is_over() {
        return web::Json(APIResult {
            success: false,
            message: "The game is over",
        });
    }

    if body.quantity <= 0 {
        return web::Json(APIResult {
            success: false,
            message: "Must buy a positive amount",
        });
    }

    // items
    if let Some(item) = user
        .game
        .market
        .get()
        .iter()
        .find(|item| item.name == body.name)
    {
        let slots_used = user.game.get_used_storage();
        if (!user.game.has_upgrade("Storage Upgrade") && body.quantity > Game::BASE_STORAGE)
            || user.game.get_max_storage() < slots_used + body.quantity
        {
            return web::Json(APIResult {
                success: false,
                message: "Buy more storage upgrades to purchase that much",
            });
        }

        let price = item.price * body.quantity;
        if user.game.money.get() < price as i64 {
            return web::Json(APIResult {
                success: false,
                message: "Not enough money for that purchase",
            });
        }

        user.game.money.set(user.game.money.get() - price as i64);
        user.game.day.set(user.game.day.get() + 1);
        let mut inventory = user.game.inventory.get();
        match inventory.iter_mut().find(|i| i.name == body.name) {
            Some(user_item) => user_item.quantity += body.quantity,
            None => inventory.push(InventoryItem {
                name: body.name.to_string(),
                quantity: body.quantity,
            }),
        };
        user.game.inventory.set(inventory);
        user.game.market.set(user.game.randomize_market());

        return web::Json(APIResult {
            success: true,
            message: "Purchase was successful",
        });
    }

    web::Json(APIResult {
        success: false,
        message: "No item found with that name",
    })
}

#[post("/upgrade")]
async fn upgrade(user: User, body: web::Form<ItemPayload>) -> Json<APIResult> {
    if user.game.is_over() {
        return web::Json(APIResult {
            success: false,
            message: "The game is over",
        });
    }

    if body.quantity <= 0 || body.quantity > 32767 {
        return web::Json(APIResult {
            success: false,
            message: "Invalid quantity",
        });
    }

    // upgrades
    if let Some(item) = crate::game::UPGRADES.iter().find(|u| u.name == body.name) {
        let mut price = item.price;

        // quantity matters for donate and storage
        if item.name == "Donate to charity" || item.name == "Storage Upgrade" {
            price *= body.quantity;
        }

        // upgrade checks
        if user.game.has_upgrade("Loan") && item.name == "Loan" {
            return web::Json(APIResult {
                success: false,
                message: "You can't take out another loan",
            });
        }
        if user.game.has_upgrade("More Commodities") && item.name == "More Commodities" {
            return web::Json(APIResult {
                success: false,
                message: "You already have access to all commodities",
            });
        }

        if user.game.money.get() < price as i64 {
            return web::Json(APIResult {
                success: false,
                message: "Not enough money",
            });
        }

        let mut upgrades = user.game.upgrades.get();
        upgrades.extend(vec![item].repeat(body.quantity as usize));
        if upgrades.len() > 32767 {
            return web::Json(APIResult {
                success: false,
                message: "Too many upgrades purchased",
            });
        }
        user.game.upgrades.set(upgrades);

        if price != 0 {
            user.game.money.set(user.game.money.get() - price as i64);
        }

        if item.name == "Storage Upgrade" {
            return web::Json(APIResult {
                success: true,
                message: "Enjoy your new storage",
            });
        } else if item.name == "More Commodities" {
            let mut market = user.game.market.get();
            market.extend(crate::game::EXTENDED_ITEMS);
            user.game.market.set(market);
            user.game.market.set(user.game.randomize_market());
            return web::Json(APIResult {
                success: true,
                message: "Enjoy your new selection",
            });
        } else if item.name == "Flag" {
            return web::Json(APIResult {
                success: true,
                message: "Hacker...",
            });
        } else if item.name == "Loan" {
            user.game.debt.set(user.game.debt.get() - item.price as i64); // since item.price is negative for loan
            return web::Json(APIResult {
                success: true,
                message: "Make sure to pay it back...",
            });
        } else if item.name == "Donate to charity" {
            return web::Json(APIResult {
                success: true,
                message: "What a nice gesture :)",
            });
        } else if item.name == "Sleep" {
            user.game.day.set(user.game.day.get() + 1);
            user.game.market.set(user.game.randomize_market());

            return web::Json(APIResult {
                success: true,
                message: "Have a nice rest...",
            });
        }
    }
    web::Json(APIResult {
        success: false,
        message: "No upgrade found with that name",
    })
}

#[post("/sell")]
async fn sell(user: User, body: web::Form<ItemPayload>) -> Json<APIResult> {
    if user.game.is_over() {
        return web::Json(APIResult {
            success: false,
            message: "The game is over",
        });
    }

    if body.quantity <= 0 {
        return web::Json(APIResult {
            success: false,
            message: "Must sell a positive amount",
        });
    }

    let market = user.game.market.get();
    let item = match market.iter().find(|item| item.name == body.name) {
        Some(item) => item,
        None => {
            return web::Json(APIResult {
                success: false,
                message: "No item found with that name",
            })
        }
    };

    let mut inventory = user.game.inventory.get();
    let mut inventory_item = match inventory.iter_mut().find(|item| item.name == body.name) {
        Some(inventory_item) => inventory_item,
        None => {
            return web::Json(APIResult {
                success: false,
                message: "You don't have any of that item",
            })
        }
    };

    if body.quantity > inventory_item.quantity {
        return web::Json(APIResult {
            success: false,
            message: "You don't have enough of that item",
        });
    }

    let price = item.price * body.quantity;

    user.game.money.set(user.game.money.get() + price as i64);
    user.game.day.set(user.game.day.get() + 1);
    inventory_item.quantity -= body.quantity;
    user.game.inventory.set(inventory);
    user.game.market.set(user.game.randomize_market());

    web::Json(APIResult {
        success: true,
        message: "Sale was successful",
    })
}

#[post("/reset")]
async fn reset(user: User) -> Json<APIResult> {
    let mut user = match crate::USERS.get_mut(&user.username) {
        Some(user) => user,
        None => {
            return web::Json(APIResult {
                success: false,
                message: "Unable to read user",
            })
        }
    };
    user.game = Game::new();
    web::Json(APIResult {
        success: true,
        message: "Reset was successful",
    })
}

pub fn routes() -> Scope {
    web::scope("/api")
        .service(buy)
        .service(sell)
        .service(upgrade)
        .service(reset)
}

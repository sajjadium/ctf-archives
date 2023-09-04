use actix_web::{error, get, web, Error, HttpResponse};
use rand::{rngs::StdRng, Rng, SeedableRng};
use serde::Serialize;
use std::sync::{Arc, Mutex};
use tera::{Context, Tera};

// thread-safe lock system
// avoids clones and copies
#[derive(Debug, Clone, Default)]
pub struct LockHelper<T> {
    value: Arc<Mutex<T>>,
}

impl<T: Clone> LockHelper<T> {
    pub fn get(&self) -> T {
        let mutex = self.value.lock().unwrap();
        mutex.clone()
    }
    pub fn set(&self, val: T) {
        let mut mutex = self.value.lock().unwrap();
        *mutex = val;
    }
    pub fn from(val: T) -> LockHelper<T> {
        LockHelper::<T> {
            value: Arc::new(Mutex::new(val)),
        }
    }
}

#[derive(Debug, Clone)]
pub struct User {
    pub username: String,
    pub password: String,
    pub game: Game,
}

impl User {
    pub fn new(username: String, password: String) -> User {
        User {
            username,
            password,
            game: Game::new(),
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct Game {
    pub day: LockHelper<i32>,
    pub market: LockHelper<Vec<Item>>,
    pub inventory: LockHelper<Vec<InventoryItem>>,
    pub upgrades: LockHelper<Vec<Upgrade>>,
    pub money: LockHelper<i64>,
    pub debt: LockHelper<i64>,
}

impl Game {
    pub const BASE_STORAGE: i32 = 100;
    pub const TOTAL_DAYS: i32 = 7;
    pub const START_MONEY: i64 = 30_000;

    pub fn new() -> Game {
        let game = Game {
            day: LockHelper::from(1),
            market: LockHelper::from(Vec::from(BASE_ITEMS)),
            inventory: LockHelper::from(Vec::new()),
            upgrades: LockHelper::from(Vec::new()),
            money: LockHelper::from(Game::START_MONEY),
            debt: LockHelper::from(0),
        };
        game.market.set(game.randomize_market());
        game
    }

    pub fn randomize_market(&self) -> Vec<Item> {
        let mut rng = StdRng::from_entropy();
        let mut market = self.market.get();
        for mut item in market.iter_mut() {
            let mut price = item.price as f64;
            price *= rng.gen_range((1.0 - item.volatility)..(1.0 + item.volatility));
            item.price = f64::max(price, 50.0).round() as i32;
        }
        market
    }

    pub fn count_upgrades(&self, name: &str) -> i32 {
        self.upgrades.get().iter().filter(|&item| item.name == name).count() as i32
    }

    pub fn has_upgrade(&self, name: &str) -> bool {
        self.count_upgrades(name) > 0
    }

    pub fn get_max_storage(&self) -> i32 {
        Game::BASE_STORAGE + Game::BASE_STORAGE * self.count_upgrades("Storage Upgrade")
    }

    pub fn get_used_storage(&self) -> i32 {
        self.inventory
            .get()
            .iter()
            .fold(0, |acc, item| item.quantity + acc)
    }

    pub fn is_over(&self) -> bool {
        return self.day.get() >= Game::TOTAL_DAYS;
    }
}

#[get("/game")]
pub async fn game_route(tera: web::Data<Tera>, user: User) -> Result<HttpResponse, Error> {
    let mut context = Context::new();
    context.insert("money", &user.game.money.get());
    context.insert("day", &user.game.day.get());
    context.insert("debt", &user.game.debt.get());

    context.insert("inventory", &user.game.inventory.get());
    context.insert("market", &user.game.market.get());

    context.insert("upgrades", &UPGRADES);
    context.insert("total_days", &Game::TOTAL_DAYS);

    context.insert(
        "storage",
        &format!(
            "{}/{}",
            &user.game.get_used_storage(),
            &user.game.get_max_storage()
        ),
    );

    if user.game.has_upgrade("Flag") {
        context.insert(
            "flag",
            &std::env::var("FLAG").unwrap_or_else(|_| "flag{test_flag}".to_string()),
        );
    }

    context.insert("game_over", &user.game.is_over());
    context.insert("donated", &user.game.count_upgrades("Donate to charity"));

    match tera.render("game.html", &context) {
        Ok(body) => Ok(HttpResponse::Ok().body(body)),
        Err(err) => Err(error::ErrorInternalServerError(err)),
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct InventoryItem {
    pub name: String,
    pub quantity: i32,
}

#[derive(Debug, Copy, Clone, Serialize)]
pub struct Item {
    pub name: &'static str,
    pub price: i32,
    pub volatility: f64,
}

#[derive(Debug, Copy, Clone, Serialize)]
pub struct Upgrade {
    pub name: &'static str,
    pub price: i32,
    pub color: &'static str, // button color
}

// list of upgrades and items
pub const UPGRADES: &[Upgrade] = &[
    Upgrade {
        name: "Storage Upgrade",
        price: 100_000,
        color: "primary",
    },
    Upgrade {
        name: "More Commodities",
        price: 100_000,
        color: "warning",
    },
    Upgrade {
        name: "Flag",
        price: 2_000_000_000,
        color: "success",
    },
    Upgrade {
        name: "Loan",
        price: -37_500,
        color: "danger",
    },
    Upgrade {
        name: "Donate to charity",
        price: 1,
        color: "info",
    },
    Upgrade {
        name: "Sleep",
        price: 0,
        color: "secondary",
    },
];

pub const BASE_ITEMS: &[Item] = &[
    Item {
        name: "Cotton",
        price: 105,
        volatility: 0.11337,
    },
    Item {
        name: "Milk",
        price: 2233,
        volatility: 0.223,
    },
    Item {
        name: "Copper",
        price: 354,
        volatility: 0.21,
    },
    Item {
        name: "Coffee",
        price: 217,
        volatility: 0.333,
    },
    Item {
        name: "Silver",
        price: 1958,
        volatility: 0.01,
    },
    Item {
        name: "Natural Gas",
        price: 780,
        volatility: 0.25,
    },
];

pub const EXTENDED_ITEMS: &[Item] = &[
    Item {
        name: "Cocoa",
        price: 23770,
        volatility: 0.543,
    },
    Item {
        name: "Gold",
        price: 167512,
        volatility: 0.792,
    },
    Item {
        name: "Palladium",
        price: 214550,
        volatility: 0.681,
    },
    Item {
        name: "Soybean",
        price: 14460,
        volatility: 0.442,
    },
    Item {
        name: "Crab",
        price: 1,
        volatility: 1.0, // lmao, why not 🦀
    },
];

use hashbrown::HashMap;
use std::fmt;
use std::io::{self};
use std::sync::mpsc::{sync_channel, Receiver};
use std::sync::{Arc, RwLock};

#[derive(Clone)]
struct Ingredient {
    vec: Arc<RwLock<Vec<u8>>>,
}

impl fmt::Display for Ingredient {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let vec = &self.vec.read().unwrap();

        for v in vec.iter() {
            write!(f, "{:02x}", v).unwrap();
        }

        write!(f, "")
    }
}

impl Drop for Ingredient {
    fn drop(&mut self) {
        /* Eat the leftovers */
        let mut calories: usize = 0;

        for v in self.vec.write().unwrap().iter_mut() {
            calories += *v as usize;
            *v = 0;
        }

        if calories > 9000 {
            panic!("FluxHorst too full! :-(");
        }
    }
}

struct BakingBook {
    recipes: [Arc<RwLock<Option<HashMap<usize, Ingredient>>>>; NUM_RECIPES],
}

impl BakingBook {
    fn add(&self, k: usize, v: HashMap<usize, Vec<u8>>) {
        let mut guarded_map = self.recipes[k].write().unwrap();

        match guarded_map.take() {
            None => {
                /* Newly created */
                guarded_map.replace(self.shareable(v));
            }
            Some(mut curr_map) => {
                if v.keys().all(|&new_key| curr_map.contains_key(&new_key)) {
                    /* All keys contained, update in place */
                    for (vec_key, vec) in v {
                        curr_map[&vec_key].vec.write().unwrap().clone_from(&vec);
                    }
                } else {
                    /* Some keys are not contained, update map */
                    curr_map.clone_from(&self.shareable(v));
                }

                guarded_map.replace(curr_map);
            }
        }
    }

    fn shareable(&self, m: HashMap<usize, Vec<u8>>) -> HashMap<usize, Ingredient> {
        m.into_iter()
            .map(|(k, v)| {
                (
                    k,
                    Ingredient {
                        vec: Arc::new(RwLock::new(v)),
                    },
                )
            })
            .collect()
    }

    fn share(&self, recipe_from: usize, ing_ind_from: usize, recipe_to: usize, ing_ind_to: usize) {
        let cp;
        {
            cp = Ingredient {
                vec: Arc::clone(
                    &self.recipes[recipe_from].read().unwrap().as_ref().unwrap()[&ing_ind_from].vec,
                ),
            };
        }
        self.recipes[recipe_to]
            .write()
            .unwrap()
            .as_mut()
            .unwrap()
            .insert(ing_ind_to, cp);
    }
}

fn worker(shared: Arc<BakingBook>, chan: Receiver<Action>) {
    loop {
        let cmd = chan.recv().unwrap();

        match cmd {
            Action::SHARE {
                recipe_from,
                ing_ind_from,
                recipe_to,
                ing_ind_to,
            } => shared.share(recipe_from, ing_ind_from, recipe_to, ing_ind_to),

            Action::ADD { k, v } => shared.add(k, v),

            Action::SHOW { recipe_no, ing_no } => {
                println!(
                    "Ing[{recipe_no}][{ing_no}] = {}",
                    shared.recipes[recipe_no].read().unwrap().as_ref().unwrap()[&ing_no]
                );
            }
        }
    }
}

fn getline(stdin: &io::Stdin, user_input: &mut String) {
    user_input.clear();
    stdin.read_line(user_input).unwrap();
    user_input.pop();
}

fn get_map_contents(stdin: &io::Stdin, user_input: &mut String) -> HashMap<usize, Vec<u8>> {
    println!("Ingredient Nums?");
    getline(stdin, user_input);

    let keys = if user_input.is_empty() {
        Vec::with_capacity(0)
    } else {
        let mut v: Vec<usize> = Vec::with_capacity(user_input.matches(",").count() + 1);
        v.extend(
            user_input
                .split(",")
                .map(|tok: &str| tok.parse::<usize>().unwrap()),
        );
        v
    };

    let mut map = HashMap::with_capacity(keys.len());

    for k in keys {
        println!("Ingredients[{k}]?");
        getline(stdin, user_input);

        let vec = if user_input.is_empty() {
            Vec::with_capacity(0)
        } else {
            let mut v = Vec::with_capacity(user_input.matches(",").count() + 1);
            v.extend(
                user_input
                    .split(",")
                    .map(|tok: &str| tok.parse::<u8>().unwrap()),
            );
            v
        };

        map.insert(k, vec);
    }

    map
}

const ADD: usize = 1;
const SHARE: usize = 2;
const SHOW: usize = 3;

enum Action {
    ADD {
        k: usize,
        v: HashMap<usize, Vec<u8>>,
    },
    SHARE {
        recipe_from: usize,
        ing_ind_from: usize,
        recipe_to: usize,
        ing_ind_to: usize,
    },
    SHOW {
        recipe_no: usize,
        ing_no: usize,
    },
}

fn get_action(stdin: &io::Stdin, user_input: &mut String) -> (usize, Action) {
    let mut worker_no: usize;
    let mut map_no: usize;
    let ing_ind_from;
    let recipe_to;
    let ing_ind_to;

    let cmd: Action = loop {
        println!("Worker?");
        getline(stdin, user_input);
        worker_no = user_input.parse::<usize>().unwrap();

        println!("Recipe?");
        getline(stdin, user_input);
        map_no = user_input.parse::<usize>().unwrap();

        println!("Action?");
        getline(stdin, user_input);
        match user_input.parse::<usize>().unwrap() {
            ADD => {
                break Action::ADD {
                    k: map_no,
                    v: get_map_contents(&stdin, user_input),
                }
            }
            SHARE => {
                println!("Source Ingredient?");
                getline(stdin, user_input);
                ing_ind_from = user_input.parse::<usize>().unwrap();

                println!("Dest Recipe?");
                getline(stdin, user_input);
                recipe_to = user_input.parse::<usize>().unwrap();

                println!("Dest Ingredient?");
                getline(stdin, user_input);
                ing_ind_to = user_input.parse::<usize>().unwrap();

                break Action::SHARE {
                    recipe_from: map_no,
                    ing_ind_from: ing_ind_from,
                    recipe_to: recipe_to,
                    ing_ind_to: ing_ind_to,
                };
            }
            SHOW => {
                println!("Ingredient?");
                getline(stdin, user_input);
                recipe_to = user_input.parse::<usize>().unwrap();

                break Action::SHOW {
                    recipe_no: map_no,
                    ing_no: recipe_to,
                };
            }
            _ => {
                println!("Unknown action...");
                continue;
            }
        }
    };
    (worker_no, cmd)
}

const NUM_WORKERS: usize = 10;
const NUM_RECIPES: usize = 10;
fn main() {
    let stdin = io::stdin();
    let mut user_input = String::with_capacity(256);

    let shared = Arc::new(BakingBook {
        recipes: Default::default(),
    });

    let mut workers = Vec::with_capacity(NUM_WORKERS);

    for _ in 0..NUM_WORKERS {
        let cloned = Arc::clone(&shared);
        let (sender, receiver) = sync_channel(0);
        workers.push(sender);
        std::thread::spawn(move || worker(cloned, receiver));
    }

    println!("Welcome! Create your very own cookie recipes.");
    println!("FluxHorst will eagerly eat your leftovers.");
    println!("He especially enjoys hashbrown'ies...");
    loop {
        let (worker_no, cmd) = get_action(&stdin, &mut user_input);
        let need_sleep = match &cmd {
            Action::SHOW {
                recipe_no: _,
                ing_no: _,
            } => true,
            _ => false,
        };
        workers[worker_no].send(cmd).unwrap();
        if need_sleep {
            std::thread::sleep(std::time::Duration::from_millis(100));
        }
    }
}

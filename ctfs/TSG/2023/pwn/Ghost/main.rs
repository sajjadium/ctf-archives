use std::io::{Read, Write};
use std::marker::PhantomData;
/// The Branded Vector Example from §2 of the paper.
/// Run from the `./ghostcell-examples` directory, with the command
/// `cargo run --example branded_vec`.

#[derive(Clone, Copy, Default)]
struct InvariantLifetime<'id>(PhantomData<*mut &'id ()>);

impl<'id> InvariantLifetime<'id> {
    #[inline]
    fn new() -> InvariantLifetime<'id> {
        InvariantLifetime(PhantomData)
    }
}

struct BrandedVec<'id, T> {
    inner: Vec<T>,
    max_index: usize,
    _marker: InvariantLifetime<'id>,
}

#[derive(Clone, Copy)]
struct BrandedIndex<'id> {
    idx: usize,
    _marker: InvariantLifetime<'id>,
}

impl<'id> std::ops::Sub<usize> for BrandedIndex<'id> {
    type Output = Self;

    fn sub(mut self, rhs: usize) -> Self::Output {
        self.idx -= rhs;
        self
    }
}

impl<'id> std::ops::Add<usize> for BrandedIndex<'id> {
    type Output = usize;

    fn add(self, rhs: usize) -> Self::Output {
        self.idx + rhs
    }
}

impl<'id, T> BrandedVec<'id, T> {
    pub fn new<R>(inner: Vec<T>, f: impl for<'id2> FnOnce(BrandedVec<'id2, T>) -> R) -> R {
        let branded_vec = BrandedVec {
            inner,
            max_index: 0,
            _marker: InvariantLifetime::new(),
        };
        f(branded_vec)
    }

    pub fn get_index(&mut self, index: usize) -> Option<BrandedIndex<'id>> {
        if index < self.inner.len() {
            if self.max_index < index {
                self.max_index = index;
            }
            Some(BrandedIndex {
                idx: index,
                _marker: InvariantLifetime::new(),
            })
        } else {
            None
        }
    }

    pub fn get(&self, index: BrandedIndex<'id>) -> &T {
        unsafe { self.inner.get_unchecked(index.idx) }
    }

    pub fn get_mut<'a>(&'a mut self, index: BrandedIndex<'id>) -> &'a mut T {
        unsafe { self.inner.get_unchecked_mut(index.idx) }
    }

    pub fn push<'a>(&'a mut self, val: T) -> BrandedIndex<'id> {
        let index = BrandedIndex {
            idx: self.inner.len(),
            _marker: InvariantLifetime::new(),
        };
        self.inner.push(val);
        index
    }

    pub fn pop<'a>(&'a mut self) {
        if self.inner.len() > self.max_index + 1 {
            self.inner.pop();
        } else {
            panic!("failed to pop")
        }
    }

    pub fn sanity_check(&self, index: BrandedIndex<'id>) -> bool {
        index.idx < self.inner.len()
    }
}

fn read_string(buf: &mut [u8]) -> usize {
    std::io::stdin().read(buf).unwrap()
}

fn get_usize() -> usize {
    let mut buf = [0; 30];
    let size = read_string(&mut buf);
    let s = unsafe { std::str::from_utf8_unchecked(&buf[..size]) };
    s.split_whitespace().next().unwrap().parse().unwrap()
}

fn print_str(s: &str) {
    print!("{s}");
    std::io::stdout().flush().expect("Unable to flush stdout");
}

struct Twitter<'id> {
    tweets: BrandedVec<'id, String>,
    pinned: BrandedIndex<'id>,
}

impl<'id> Twitter<'id> {
    fn new(f: impl for<'id2> FnOnce(Twitter<'id2>)) {
        BrandedVec::new(Vec::new(), |mut v| {
            let id = v.push("This is my first tweet!".to_string());
            f(Twitter {
                tweets: v,
                pinned: id,
            })
        });
    }
    fn post_tweet(&mut self) {
        print_str("tweet > ");
        let mut buf = [0u8; 280];
        let size = read_string(&mut buf);
        let tweet = unsafe { std::str::from_utf8_unchecked(&buf[..size]) };
        self.tweets.push(tweet.to_string());
    }
    fn undo_tweet(&mut self) {
        self.tweets.pop();
    }
    fn pin_tweet(&mut self) {
        print_str("id > ");
        let id = get_usize();
        self.pinned = self.tweets.get_index(id).expect("no such tweet");
    }
    fn move_pin_tweet(&mut self) {
        print_str("older[0] / newer[1] > ");
        let old_new = get_usize();
        print_str("size > ");
        let id = get_usize();

        if old_new == 1 {
            self.pinned = self
                .tweets
                .get_index(self.pinned + id)
                .expect("no such tweet");
        } else {
            self.pinned = self.pinned - id;
        }
        assert!(self.sanity_check());
    }
    fn print_pin(&self) {
        let tweet = self.tweets.get(self.pinned);
        print_str(tweet.as_str());
        print_str("\n");
    }
    fn modify_pin(&mut self) {
        print_str("tweet > ");

        let tweet = self.tweets.get_mut(self.pinned);
        read_string(unsafe { tweet.as_mut_vec() });
    }
    fn show_menu(&self) {
        println!("1. post tweet");
        println!("2. undo tweet");
        println!("3. pin tweet");
        println!("4. print pinned tweet");
        println!("5. modify pinned tweet");
        println!("6. move pinned tweet");
        println!("7. exit");
    }
    fn handle(&mut self) -> bool {
        print_str("> ");
        let opt = get_usize();
        match opt {
            1 => self.post_tweet(),
            2 => self.undo_tweet(),
            3 => self.pin_tweet(),
            4 => self.print_pin(),
            5 => self.modify_pin(),
            6 => self.move_pin_tweet(),
            _ => return false,
        };
        true
    }
    fn sanity_check(&self) -> bool {
        self.tweets.sanity_check(self.pinned)
    }
}

fn main() {
    Twitter::new(|mut twitter| {
        twitter.show_menu();
        let mut cont = true;
        while cont {
            cont = twitter.handle();
        }
    });
}

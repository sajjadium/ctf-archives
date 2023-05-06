// type Key = u32;
const NUM_BINS: usize = 16;
const MAX_BINSIZE: usize = 16;

use std::ptr;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;
use std::cmp::Eq;

fn calculate_hash<T: Hash + Eq>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

struct Entry<K: Hash + Eq, V> {
    key: K,
    val: V,
    next: *mut Entry<K, V>
}


struct Slot<K: Hash + Eq, V> {
    entry: *mut Entry<K, V>,
    count: usize
}

impl<K: Hash + Eq, V> Drop for Slot<K, V> {
    fn drop(&mut self) {
        let mut cur = self.entry;
        while !cur.is_null() {
            unsafe {
                let e = Box::from_raw(cur);
                cur = (*e).next;
                // println!("Slot, dropping {}", e.val);
                // explicitly free each Entry
                drop(e);
            }
        }
    }
}

impl<K: Hash + Eq, V> Slot<K, V> {
    fn add(&mut self, k: K, val: V) {
        assert!(self.get(&k).is_none(), "Duplicate key");
        assert!(self.count < MAX_BINSIZE, "Bin full");
        self.entry = Box::into_raw(
            Box::new(Entry {
                key: k,
                val: val,
                next: self.entry
            })
        );
        self.count += 1;
    }

    fn get_mut<'a>(&'a mut self, k: &K) -> Option<&'a mut V> {
        let mut cur = self.entry;
        while !cur.is_null()  {
            unsafe {
                if (*cur).key == *k {
                    return Some(&mut (*cur).val)
                }
                cur = (*cur).next
            }
        }
        None
    }

    fn get<'a>(&'a self, k: &K) -> Option<&'a V> {
        let mut cur = self.entry;
        while !cur.is_null()  {
            unsafe {
                if (*cur).key == *k {
                    return Some(& (*cur).val)
                }
                cur = (*cur).next
            }
        }
        None
    }

    // maps values in-place
    fn map_values<F>(&mut self, mut f: F) where F: (FnMut(&K, V) -> V) + Copy {
        let mut cur = self.entry;
        while !cur.is_null()  {
            unsafe {
                let mut e = ptr::read(cur);

                // map
                e.val = f(&e.key, e.val);
                
                ptr::write(cur, e);
                cur = (*cur).next;
            }
        }
    }
}

impl<K: Hash + Eq, V> Default for Slot<K, V> {
    fn default() -> Self {
        Slot {
            entry: ptr::null_mut(),
            count: 0
        }
    }
}

pub struct Store<K: Hash + Eq, V> {
    slots: [Slot<K, V>; NUM_BINS]
}

impl<K: Hash + Eq, V> Store<K, V> {
    fn get_bin(&self, k: &K) -> &Slot<K, V> {
        let bin_num = (calculate_hash(&k) as usize) % NUM_BINS;
        &self.slots[bin_num]
    }

    fn get_bin_mut(&mut self, k: &K) -> &mut Slot<K, V> {
        let bin_num = (calculate_hash(&k) as usize) % NUM_BINS;
        &mut self.slots[bin_num]
    }

    pub fn set(&mut self, k: K, val: V) {
        // let boxed = Box::new(val);
        self.get_bin_mut(&k).add(k, val);
    }

    pub fn get(&self, k: &K) -> Option<&V> {
        return self.get_bin(k).get(k);
    }

    pub fn get_mut(&mut self, k: &K) -> Option<&mut V> {
        return self.get_bin_mut(k).get_mut(k);
    }

    pub fn map_values<F>(&mut self, f: F) where F: (FnMut(&K, V) -> V) + Copy {
        for slot in &mut self.slots {
            slot.map_values(f);
        }
    }

    pub fn new() -> Store<K, V> {
        Store { 
            slots: Default::default()
        }
    }
}

use libc::c_uint;
use std::collections::{HashMap,BTreeMap};

pub struct Maps {
    pub allocs: [c_uint; 10],
    pub results: [c_uint; 10],
    pub maps: [*mut MapWrap; 10],
}

const ALLOC_RUST_BTREEMAP: c_uint = 1;
const ALLOC_RUST_HASHMAP: c_uint = 2;

pub enum MapWrap {
    HASHMAP {
        m: HashMap<c_uint, c_uint>
    },
    BTREEMAP {
        m: BTreeMap<c_uint, c_uint>
    }
}

#[no_mangle]
pub extern "C" fn init(maps: &mut Maps) {
    maps.allocs = Default::default();
    maps.maps = [std::ptr::null_mut(); 10];
    maps.results = Default::default();
}

#[no_mangle]
pub extern "C" fn create(maps: &mut Maps, ind: c_uint, map_type: c_uint) {
    match map_type {
        ALLOC_RUST_HASHMAP => {
            maps.maps[ind as usize] = Box::into_raw(Box::new(MapWrap::HASHMAP {
                    m: HashMap::new()
            }))
        },
        ALLOC_RUST_BTREEMAP => {
            maps.maps[ind as usize] = Box::into_raw(Box::new(MapWrap::BTREEMAP {
                m: BTreeMap::new()
        }))
        },
        _ => unreachable!()
    }
}

#[no_mangle]
pub extern "C" fn destroy(maps: &mut Maps, ind: c_uint) {
    assert!(!maps.maps[ind as usize].is_null());

    let ptr = maps.maps[ind as usize];
    drop(unsafe { Box::from_raw(ptr) });
    maps.maps[ind as usize] = std::ptr::null_mut();
}

#[no_mangle]
pub extern "C" fn get(maps: &Maps, ind: c_uint, k: c_uint) -> c_uint {
    let ptr = maps.maps[ind as usize];
    let m = unsafe { ptr.as_ref() }.unwrap();

    match m {
        MapWrap::HASHMAP { m } => {
            *m.get(&k).unwrap()
        }
        MapWrap::BTREEMAP { m } => {
            *m.get(&k).unwrap()
        }
    }
}

#[no_mangle]
pub extern "C" fn put(maps: &mut Maps, ind: c_uint, k: c_uint, v: c_uint) {
    let ptr = maps.maps[ind as usize];
    let m = unsafe { ptr.as_mut() }.unwrap();

    match m {
        MapWrap::HASHMAP { m } => {
            m.insert(k, v)
        }
        MapWrap::BTREEMAP { m } => {
            m.insert(k, v)
        }
    };
}

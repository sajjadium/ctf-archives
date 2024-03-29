use base64::{engine::general_purpose, Engine as _};
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::mem;
use wasm_bindgen::prelude::*;

pub const STATIC_UNIT: &&() = &&();

#[inline(never)]
pub fn translate<'a, 'b, T>(_val_a: &'a &'b (), val_b: &'b mut T) -> &'a mut T {
	val_b
}

pub fn expand_mut<'a, 'b, T>(x: &'a mut T) -> &'b mut T {
	let f: fn(_, &'a mut T) -> &'b mut T = translate;
	f(STATIC_UNIT, x)
}

pub fn transmute<A, B>(obj: A) -> B {
	use std::hint::black_box;

	enum TransmuteEnum<A, B> {
		A(Option<Box<A>>),
		B(Option<Box<B>>),
	}

	#[inline(never)]
	fn transmute_inner<A, B>(trans: &mut TransmuteEnum<A, B>, obj: A) -> B {
		let TransmuteEnum::B(ref_to_b) = trans else {
			unreachable!()
		};
		let ref_to_b = expand_mut(ref_to_b);
		*trans = TransmuteEnum::A(Some(Box::new(obj)));
		black_box(trans);

		*ref_to_b.take().unwrap()
	}

	transmute_inner(black_box(&mut TransmuteEnum::B(None)), obj)
}

#[inline(always)]
pub fn make_string(ptr: *mut u8, cap: usize, len: usize) -> String {
	let sentinel_string = crate::transmute::<_, String>([0usize, 1usize, 2usize]);

	let mut actual_buf = [0usize; 3];
	actual_buf[sentinel_string.as_ptr() as usize] = ptr as usize;
	actual_buf[sentinel_string.capacity()] = cap;
	actual_buf[sentinel_string.len()] = len;

	std::mem::forget(sentinel_string);

	crate::transmute::<_, String>(actual_buf)
}

#[wasm_bindgen]
#[inline(never)]
pub fn encrypt(input_ref: &str) -> String {
    let input: String = input_ref.into();

    let seed: [u8; 32] = [0xde, 0xed, 0xbe, 0xef, 0xfe, 0xed, 0xba, 0x0c, 0xca, 0xb0, 0xb0, 0xb5, 0xde, 0xfa, 0xce, 0x0d, 0xca, 0xfe, 0xb0, 0xba, 0xde, 0xad, 0xc0, 0xde, 0xfe, 0xe1, 0xde, 0xad, 0xde, 0xad, 0x10, 0xcc];
    let mut rng: StdRng = SeedableRng::from_seed(seed);

    let encrypted_input: String = input
        .chars()
        .map(|c| (c as u8) ^ (rng.gen::<u8>()))
        .map(|c| c as char)
        .collect();

    let encrypted_input_b64 = general_purpose::STANDARD.encode(&encrypted_input.as_bytes());
    
    return encrypted_input_b64;
}

#[wasm_bindgen]
#[inline(never)]
pub fn decrypt(input_ref: &str) -> String {
    #[repr(C)]
    struct ProgramState {
        last_decryption: [u8; 300],
        success_msg: [u8; 300],
        failure_msg: [u8; 300],
    }

    let mut state: ProgramState = std::hint::black_box(ProgramState {
        last_decryption: [0u8; 300],
        success_msg: [0u8; 300],
        failure_msg: [0u8; 300],
    });
    let success = [b's', b'u', b'c', b'c', b'e', b's', b's'];
    let failure = [b'f', b'a', b'i', b'l', b'u', b'r', b'e'];
    state.success_msg[..7].copy_from_slice(&success);
    state.failure_msg[..7].copy_from_slice(&failure);

    let input_vector = general_purpose::STANDARD.decode(input_ref.as_bytes()).unwrap();
    let input = String::from_utf8_lossy(&input_vector);
    let seed: [u8; 32] = [0xde, 0xed, 0xbe, 0xef, 0xfe, 0xed, 0xba, 0x0c, 0xca, 0xb0, 0xb0, 0xb5, 0xde, 0xfa, 0xce, 0x0d, 0xca, 0xfe, 0xb0, 0xba, 0xde, 0xad, 0xc0, 0xde, 0xfe, 0xe1, 0xde, 0xad, 0xde, 0xad, 0x10, 0xcc];
    let mut rng: StdRng = SeedableRng::from_seed(seed);

    let decrypted_string: String = input
        .chars()
        .map(|c| (c as u8) ^ (rng.gen::<u8>()))
        .map(|c| c as char)
        .collect();

	let mut last_decryption = make_string(state.last_decryption.as_mut_ptr(), 600usize, 0usize);
    last_decryption.push_str(&decrypted_string);
    mem::forget(last_decryption);

    let decryption_msg: String;
    if decrypted_string.len() > 0 {
        decryption_msg = String::from_utf8_lossy(&state.success_msg).to_string();
    } else {
        decryption_msg = String::from_utf8_lossy(&state.failure_msg).to_string();
    }
    return decryption_msg;
}

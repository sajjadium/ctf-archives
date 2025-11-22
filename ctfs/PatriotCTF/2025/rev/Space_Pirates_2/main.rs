/*
 * SPACE PIRATES CTF CHALLENGE - LEVEL 2: THE TREASURE MAP
 * ========================================================
 * You decoded the coordinates and found the pirates' 
 * hidden base. Now you've discovered their treasure map, but it's encrypted 
 * with an even MORE complex cipher. The pirates learned from their mistake 
 * and upgraded their security!
 * 
 */

use std::env;
use std::process;

// The target encrypted treasure map (what we want the transformed input to become)
const TARGET: [u8; 32] = [
    0x15, 0x5A, 0xAC, 0xF6, 0x36, 0x22, 0x3B, 0x52, 0x6C, 0x4F, 0x90, 0xD9, 0x35, 0x63, 0xF8, 0x0E, 0x02, 0x33, 0xB0, 0xF1, 0xB7, 0x69, 0x42, 0x67, 0x25, 0xEA, 0x96, 0x63, 0x1B, 0xA7, 0x03, 0x0B
];

// The pirate's NEW rotating XOR key (upgraded security!)
const XOR_KEY: [u8; 5] = [0x7E, 0x33, 0x91, 0x4C, 0xA5];

// NEW: Rotation amounts for each position modulo 7
const ROTATION_PATTERN: [u32; 7] = [1, 3, 5, 7, 2, 4, 6];

// The magic subtraction constant (they switched from addition!)
const MAGIC_SUB: u8 = 0x5D;

//input: &str
fn print_flag(buffer: &str) {
    println!("\n╔══════════════════════════════════════════╗");
    println!("║                                          ║");
    println!("║     _______________                      ║");
    println!("║    /               \\                     ║");
    println!("║   /  💎  💰  💎  💰  \\                    ║");
    println!("║  |   💰  💎  💰  💎   |                   ║");
    println!("║  |  💎 TREASURE! 💎  |                   ║");
    println!("║  |   💰  💎  💰  💎   |                   ║");
    println!("║   \\  💎  💰  💎  💰  /                    ║");
    println!("║    \\_______________ /                    ║");
    println!("║         |     |                          ║");
    println!("║         |_____|                          ║");
    println!("║                                          ║");
    println!("╚══════════════════════════════════════════╝");
    println!("\n🏴‍☠️  LEVEL 2 COMPLETE! YOU FOUND THE TREASURE! 🏴‍☠️\n");
    println!("The pirates' secret hoard is yours!\n");
    println!("Flag: {0}\n", buffer);
    println!("You've mastered the advanced pirate cipher!");
    println!("The treasure contains riches beyond imagination!\n");
}

/// Rotate a byte left by n positions
/// This is a bijection because all 8 bit rotations of a byte are unique
/// ROL(ROL(x, n), 8-n) = x, proving invertibility
fn rotate_left(byte: u8, n: u32) -> u8 {
    byte.rotate_left(n % 8)
}

/// OPERATION 1: XOR with NEW rotating key
/// Each byte is XORed with one of 5 NEW key bytes (cycling through them)
/// Bijection proof: (x ⊕ k) ⊕ k = x (XOR involution)
fn apply_quantum_cipher_v2(buffer: &mut [u8]) {
    for (i, byte) in buffer.iter_mut().enumerate() {
        *byte ^= XOR_KEY[i % 5];
    }
}

/// OPERATION 2 (NEW!): Rotate Left with varying amounts
/// Each byte is rotated left by an amount determined by its position
/// Bijection proof: ROL⁻¹ = ROR with same amount
/// The rotation amount varies: position mod 7 selects from ROTATION_PATTERN
fn apply_stellar_rotation(buffer: &mut [u8]) {
    for (i, byte) in buffer.iter_mut().enumerate() {
        let rotation = ROTATION_PATTERN[i % 7];
        *byte = rotate_left(*byte, rotation);
    }
}

/// OPERATION 3: Swap adjacent byte pairs
/// Bytes at positions (0,1), (2,3), (4,5), etc. are swapped
/// Bijection proof: Swapping twice returns original (f ∘ f = identity)
fn apply_spatial_transposition(buffer: &mut [u8]) {
    for i in (0..buffer.len()).step_by(2) {
        buffer.swap(i, i + 1);
    }
}

/// OPERATION 4: Subtract magic constant (mod 256) - CHANGED FROM ADDITION!
/// Each byte has MAGIC_SUB subtracted from it (wrapping at 256)
/// Bijection proof: (x - k) + k ≡ x (mod 256)
/// Subtraction forms a group, every element has unique inverse
fn apply_gravitational_shift_v2(buffer: &mut [u8]) {
    for byte in buffer.iter_mut() {
        *byte = byte.wrapping_sub(MAGIC_SUB);
    }
}

/// OPERATION 5 (NEW!): Reverse bytes in chunks of 5
/// Splits the 30-byte buffer into 6 chunks of 5, reverses each chunk
/// Chunk 0: [0,1,2,3,4] -> [4,3,2,1,0]
/// Chunk 1: [5,6,7,8,9] -> [9,8,7,6,5], etc.
/// Bijection proof: Reversal is self-inverse, f(f(x)) = x
fn apply_temporal_inversion(buffer: &mut [u8]) {
    const CHUNK_SIZE: usize = 5;
    for chunk_start in (0..buffer.len()).step_by(CHUNK_SIZE) {
        let chunk_end = (chunk_start + CHUNK_SIZE).min(buffer.len());
        buffer[chunk_start..chunk_end].reverse();
    }
}

/// OPERATION 6 (NEW!): XOR each byte with its position SQUARED (mod 256)
/// Byte at position i is XORed with i² mod 256
/// Bijection proof: (x ⊕ k) ⊕ k = x (XOR involution)
/// While i² grows, mod 256 keeps values in range, and XOR remains invertible
fn apply_coordinate_calibration_v2(buffer: &mut [u8]) {
    for (i, byte) in buffer.iter_mut().enumerate() {
        // Square the position and take mod 256 to keep it in u8 range
        let position_squared = ((i * i) % 256) as u8;
        *byte ^= position_squared;
    }
}

fn process_transmission(input: &str) -> Result<[u8; 32], String> {
    // Validate length
    if input.len() != 32 {
        return Err(format!(
            "Invalid treasure map length!\n   Got {} bytes, expected 32 bytes\n   Hint: Treasure maps have specific coordinate formats",
            input.len()
        ));
    }

    // Convert to byte array
    let mut buffer = [0u8; 32];
    buffer.copy_from_slice(input.as_bytes());

    println!("Decrypting treasure map...\n");

    println!("[1/6] Applying advanced quantum entanglement cipher...");
    apply_quantum_cipher_v2(&mut buffer);

    println!("[2/6] Applying stellar rotation transformation...");
    apply_stellar_rotation(&mut buffer);

    println!("[3/6] Applying spatial transposition...");
    apply_spatial_transposition(&mut buffer);

    println!("[4/6] Applying inverse gravitational shift...");
    apply_gravitational_shift_v2(&mut buffer);

    println!("[5/6] Applying temporal inversion...");
    apply_temporal_inversion(&mut buffer);

    println!("[6/6] Applying advanced coordinate calibration...");
    apply_coordinate_calibration_v2(&mut buffer);

    Ok(buffer)
}

fn main() {
    println!("╔═══════════════════════════════════════════╗");
    println!("║  SPACE PIRATES TREASURE MAP DECODER v2.0  ║");
    println!("║              LEVEL 2: ADVANCED            ║");
    println!("╚═══════════════════════════════════════════╝");
    println!("\n Welcome back, treasure hunter!");
    println!("You cracked the coordinates, but now you need");
    println!("to decrypt the actual TREASURE MAP!");
    println!("\n  WARNING: The pirates upgraded their cipher!");

    // Get command line arguments
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        eprintln!(" Usage: {} <encrypted_treasure_map>", args[0]);
        eprintln!("   Example: {} TREASURE_MAP_ALPHA_12345678901", args[0]);
        process::exit(1);
    }

    let input = &args[1];

    // Process the transmission
    match process_transmission(input) {
        Ok(buffer) => {
            println!("\nVerifying treasure map authenticity...");

            // Check if the result matches our target
            if buffer == TARGET {
                print_flag(input);
            } else {
                println!("\n DECRYPTION FAILED!\n");
                println!("This doesn't match any known treasure map format.");
                println!("Hint: Pirates use numeric codes mixed with text...\n");

                // Debug output (helpful for solving)
                // print!("Your result (hex): ");
                // for byte in buffer.iter() {
                //     print!("0x{:02X}, ", byte);
                // }
                println!("\n");
                process::exit(1);
            }
        }
        Err(err) => {
            eprintln!(" {}", err);
            process::exit(1);
        }
    }
}

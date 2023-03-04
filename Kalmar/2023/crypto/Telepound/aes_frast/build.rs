use std::env;
use std::fs;
use std::path::Path;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    let out_dir = env::var_os("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("tables.rs");
    let tables_txt = calculate_tables();
    fs::write(&dest_path, tables_txt).unwrap();
}
fn calculate_tables() -> String {
    use crate::aes_affine_mapping::aes_sbox_affine_mapping as affine_mapping;
    use crate::aes_affine_mapping::aes_sbox_inverse_affine_mapping as inverse_mapping;
    use crate::gf28::GF2_8;
    use crate::t_box::*;
    // A GF2_8 for computing the tables.
    let mut gf = GF2_8::default();
    // Another two GF2_8 for storing the S-Boxed `gf` and inverse-S-Boxed `gf`.
    let mut substitued_gf = GF2_8::default();
    let mut invrsboxed_gf: GF2_8;
    // Three strings for Rust code of SBox and something output.
    let mut sboxtable_code = String::with_capacity(2048);
    sboxtable_code.push_str("// S-Box\nstatic SBOX: &[u8; 256] = &[\n");
    let mut inversetable_code = String::with_capacity(2048);
    inversetable_code.push_str("// Inversed S-Box\nstatic SINV: &[u8; 256] = &[\n");
    //Eight strings for Rust code of TBoxes output.
    let mut e_t0_code = String::with_capacity(4096);
    e_t0_code.push_str("// T-Box 0 for encryption\nstatic TE0: &[u32; 256] = &[\n");
    let mut e_t1_code = String::with_capacity(4096);
    e_t1_code.push_str("// T-Box 1 for encryption\nstatic TE1: &[u32; 256] = &[\n");
    let mut e_t2_code = String::with_capacity(4096);
    e_t2_code.push_str("// T-Box 2 for encryption\nstatic TE2: &[u32; 256] = &[\n");
    let mut e_t3_code = String::with_capacity(4096);
    e_t3_code.push_str("// T-Box 3 for encryption\nstatic TE3: &[u32; 256] = &[\n");
    let mut d_t0_code = String::with_capacity(4096);
    d_t0_code.push_str("// T-Box 0 for decryption\nstatic TD0: &[u32; 256] = &[\n");
    let mut d_t1_code = String::with_capacity(4096);
    d_t1_code.push_str("// T-Box 1 for decryption\nstatic TD1: &[u32; 256] = &[\n");
    let mut d_t2_code = String::with_capacity(4096);
    d_t2_code.push_str("// T-Box 2 for decryption\nstatic TD2: &[u32; 256] = &[\n");
    let mut d_t3_code = String::with_capacity(4096);
    d_t3_code.push_str("// T-Box 3 for decryption\nstatic TD3: &[u32; 256] = &[\n");
    // Three variables to temporarily store numbers.
    let mut inverse: u8;
    #[allow(non_snake_case)]
    let mut afterAM: u8;
    let mut invsbox: u8;
    let mut number: u8;
    for m in 0..16 {
        sboxtable_code.push_str("    ");
        inversetable_code.push_str("    ");
        e_t0_code.push_str("    ");
        e_t1_code.push_str("    ");
        e_t2_code.push_str("    ");
        e_t3_code.push_str("    ");
        d_t0_code.push_str("    ");
        d_t1_code.push_str("    ");
        d_t2_code.push_str("    ");
        d_t3_code.push_str("    ");
        for n in 0..16 {
            number = (m << 4) | n;
            gf.set(number);
            inverse = gf.inverse().unwrap_or_default().get_byte();
            afterAM = affine_mapping(inverse);
            substitued_gf.set(afterAM);
            // Although the table of the inversed S-Box can be Obtained by looking up
            // S-Box table inversely, it doesn't hurt to know compute it with matrix
            // for studying AES.
            gf.set(inverse_mapping(number));
            invrsboxed_gf = gf.inverse().unwrap_or_default();
            invsbox = invrsboxed_gf.get_byte();
            sboxtable_code.push_str(format!("0x{:02X}, ", afterAM).as_str());
            inversetable_code.push_str(format!("0x{:02X}, ", invsbox).as_str());
            e_t0_code.push_str(format!("0x{:08X}, ", e_t0_element(&substitued_gf)).as_str());
            e_t1_code.push_str(format!("0x{:08X}, ", e_t1_element(&substitued_gf)).as_str());
            e_t2_code.push_str(format!("0x{:08X}, ", e_t2_element(&substitued_gf)).as_str());
            e_t3_code.push_str(format!("0x{:08X}, ", e_t3_element(&substitued_gf)).as_str());
            d_t0_code.push_str(format!("0x{:08X}, ", d_t0_element(&invrsboxed_gf)).as_str());
            d_t1_code.push_str(format!("0x{:08X}, ", d_t1_element(&invrsboxed_gf)).as_str());
            d_t2_code.push_str(format!("0x{:08X}, ", d_t2_element(&invrsboxed_gf)).as_str());
            d_t3_code.push_str(format!("0x{:08X}, ", d_t3_element(&invrsboxed_gf)).as_str());
            if n == 7 {
                e_t0_code.pop();
                e_t0_code.push_str("\n    ");
                e_t1_code.pop();
                e_t1_code.push_str("\n    ");
                e_t2_code.pop();
                e_t2_code.push_str("\n    ");
                e_t3_code.pop();
                e_t3_code.push_str("\n    ");
                d_t0_code.pop();
                d_t0_code.push_str("\n    ");
                d_t1_code.pop();
                d_t1_code.push_str("\n    ");
                d_t2_code.pop();
                d_t2_code.push_str("\n    ");
                d_t3_code.pop();
                d_t3_code.push_str("\n    ");
            }
        }
        sboxtable_code.pop();
        sboxtable_code.push('\n');
        inversetable_code.pop();
        inversetable_code.push('\n');
        e_t0_code.pop();
        e_t0_code.push('\n');
        e_t1_code.pop();
        e_t1_code.push('\n');
        e_t2_code.pop();
        e_t2_code.push('\n');
        e_t3_code.pop();
        e_t3_code.push('\n');
        d_t0_code.pop();
        d_t0_code.push('\n');
        d_t1_code.pop();
        d_t1_code.push('\n');
        d_t2_code.pop();
        d_t2_code.push('\n');
        d_t3_code.pop();
        d_t3_code.push('\n');
    }
    sboxtable_code.push_str("];\n");
    inversetable_code.push_str("];\n");
    e_t0_code.push_str("];\n");
    e_t1_code.push_str("];\n");
    e_t2_code.push_str("];\n");
    e_t3_code.push_str("];\n");
    d_t0_code.push_str("];\n");
    d_t1_code.push_str("];\n");
    d_t2_code.push_str("];\n");
    d_t3_code.push_str("];\n");
    let mut final_out = String::with_capacity(32768);
    final_out.push_str(&sboxtable_code);
    final_out.push_str(&inversetable_code);
    final_out.push_str(&e_t0_code);
    final_out.push_str(&e_t1_code);
    final_out.push_str(&e_t2_code);
    final_out.push_str(&e_t3_code);
    final_out.push_str(&d_t0_code);
    final_out.push_str(&d_t1_code);
    final_out.push_str(&d_t2_code);
    final_out.push_str(&d_t3_code);
    // Compute the addend (round coefficient) needed in the round function.
    let x = GF2_8::new(0b_0000_0010);
    let mut a = GF2_8::new(0b_0000_0001);
    final_out.push_str(
        "// Addend (round coefficient) needed in the round function\nconst RC: &[u8; 10] = &[\n    ",
    );
    final_out.push_str(format!("0x{:02X},\n", a.get_byte()).as_str());
    for _ in 1..10 {
        a = x * a;
        final_out.push_str(format!("    0x{:02X},\n", a.get_byte()).as_str());
    }
    final_out.push_str("];\n");
    final_out
}
mod gf28 {
    //! # gf28
    //! `GF2_8` is one of foundamental structures for low-level compution of AES S-box, though many fast
    //! implements now use look-up-table.
    use std::fmt;
    use std::ops::{Add, Div, Mul, Sub};
    // There is a small difference between `derive` and `impl` manually.
    // https://doc.rust-lang.org/std/marker/trait.Copy.html#how-can-i-implement-copy
    #[allow(non_camel_case_types)]
    #[derive(Copy, Clone)]
    pub struct GF2_8 {
        inner: u8,
    }
    impl Default for GF2_8 {
        /// The default value of GF2_8 is `GF2_8 {inner: 0b_0000_0000u8}`.
        fn default() -> Self {
            Self { inner: 0u8 }
        }
    }
    // AES standard use this inrreducible polynomial:
    // x^8 + x^4 + x^3 + x + 1
    const IRREDU_POLYNO: u16 = 0b_1_0001_1011;
    /// Bitwise multipl and mod for inner u16 computing.  
    /// Like a function parameters, the pattern should be `(left: u16, right: u16)`.  
    /// And this returns `u16`.
    macro_rules! bitwise_multiply_with_mod {
        ($left:expr, $right:expr) => {{
            let mut result: u16 = 0;
            let mut digit: u16 = 1;
            for i in 0..8 {
                if (digit & $right) != 0 {
                    result ^= $left << i;
                }
                digit <<= 1;
            }
            // when result >= 2^8 need MOD
            if result >= 0b_1_0000_0000 {
                let modp = IRREDU_POLYNO << 6;
                digit <<= 6;
                for i in 0..7 {
                    if (digit & result) != 0 {
                        result ^= modp >> i;
                    }
                    digit >>= 1;
                }
            }
            result
        }};
    }
    /// Bitwise divide for inner u16 computing.  
    /// This function retures `(quotient, reminder)`.  
    /// Like a function parameters, the pattern should be `(dividend: u16, divisor: u16)`.  
    /// And this returns `(quotient: u16, reminder: u16)`.
    macro_rules! bitwise_divide {
        ($dividend:expr, $divisor:expr) => {{
            let mut shift = $divisor.leading_zeros() - 7;
            let divisor: u16 = $divisor << shift;
            shift += 1;
            let mut reminder: u16 = $dividend;
            let mut quotient: u16 = 0;
            let mut digit: u16 = 0b_1_0000_0000;
            for i in 0..shift {
                if (digit & reminder) != 0 {
                    reminder ^= divisor >> i;
                    // Bitwise operator is a little faster than add operator. They achieve the same
                    // effect because there is no need to carry. So I use `^=` instead of `+=` here.
                    // In fact, in this case, because there will never be `1 op 1` (as a result of
                    // shifting bits), using `|=` as the `op` is ok.
                    quotient ^= 1;
                }
                quotient <<= 1;
                digit >>= 1;
            }
            quotient >>= 1;
            (quotient, reminder)
        }};
    }
    impl GF2_8 {
        /// Create a new GF2_8 from a u8 value.
        pub fn new(value: u8) -> Self {
            Self { inner: value }
        }
        /// Get the inner value of a GF2_8 as u8.
        pub fn get_byte(&self) -> u8 {
            self.inner
        }
        /// Set the inner value of a GF2_8.
        pub fn set(&mut self, value: u8) {
            self.inner = value;
        }
        /// Get the inverse of a GF2_8.  
        /// This is implemented by calculating using the Extended Euclidean Algorithm.  
        /// Note that 0 has no inverse, so this function will return `None`.
        pub fn inverse(&self) -> Option<Self> {
            if self.inner >= 2u8 {
                let mut t2: u16 = 0u16;
                let mut t1: u16 = 1u16;
                let mut r2: u16 = IRREDU_POLYNO;
                let mut r1: u16 = self.inner as u16;
                let mut tmp: u16;
                while r1 != 0u16 {
                    let (quotient, reminder) = bitwise_divide!(r2, r1);
                    tmp = t2 ^ bitwise_multiply_with_mod!(quotient, t1);
                    r2 = r1;
                    r1 = reminder;
                    t2 = t1;
                    t1 = tmp;
                }
                Some(Self { inner: t2 as u8 })
            } else if self.inner == 1u8 {
                Some(*self)
            } else {
                None
            }
        }
    }
    impl fmt::Display for GF2_8 {
        /// Format the inner value of GF2_8 as 8bit binary.
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            write!(f, "{:08b}", self.inner)
        }
    }
    impl Add for GF2_8 {
        type Output = Self;
        /// Add operator.
        fn add(self, other: Self) -> Self {
            Self {
                inner: self.inner ^ other.inner,
            }
        }
    }
    impl Sub for GF2_8 {
        type Output = Self;
        /// Subtact operator. In fact this is the same as its add operator.
        fn sub(self, other: Self) -> Self {
            Self {
                inner: self.inner ^ other.inner,
            }
        }
    }
    impl Mul for GF2_8 {
        type Output = Self;
        /// Multiply operator. MOD by AES standard inrreducible polynomial.  
        /// This is implemented by multiplying bitwisely, rather than looking up table calculated
        /// from GF generators.
        fn mul(self, other: Self) -> Self {
            Self {
                inner: bitwise_multiply_with_mod!(self.inner as u16, other.inner as u16) as u8,
            }
        }
    }
    impl Div for GF2_8 {
        type Output = Self;
        /// Divide operator.  
        /// This uses the definition that `a / b == a * b.inverse()`.  
        /// Note that 'divided by zero' will lead to `panic!`.
        fn div(self, other: Self) -> Self {
            if other.inner != 1 {
                self * other.inverse().expect("0 has no inverse.")
            } else {
                Self { inner: self.inner }
            }
        }
    }
    #[cfg(test)]
    mod tests {
        use super::GF2_8;
        // There are some redundant code.
        // To make the code easy to understand, I didn't put them in a Rust-lang macro.
        #[test]
        fn basics_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            assert_eq!(foo.inner, 0b_1000_0000);
            foo.set(0b_0000_0010);
            assert_eq!(foo.get_byte(), 0b_0000_0010);
        }
        #[test]
        fn add_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            let mut bar = GF2_8::new(0b_0000_0010);
            assert_eq!((foo + bar).inner, 0b_1000_0010);
            foo = GF2_8::new(0b_1100_0010);
            bar = GF2_8::new(0b_0010_1111);
            assert_eq!((foo + bar).inner, 0b_1110_1101);
        }
        #[test]
        fn sub_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            let mut bar = GF2_8::new(0b_0000_0010);
            assert_eq!((foo - bar).inner, 0b_1000_0010);
            foo = GF2_8::new(0b_1100_0010);
            bar = GF2_8::new(0b_0010_1111);
            assert_eq!((foo - bar).inner, 0b_1110_1101);
        }
        #[test]
        fn mul_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            let mut bar = GF2_8::new(0b_0000_0010);
            assert_eq!((foo * bar).inner, 0b_0001_1011);
            foo = GF2_8::new(0b_1100_0010);
            bar = GF2_8::new(0b_0010_1111);
            assert_eq!((foo * bar).inner, 0b_0000_0001);
        }
        #[test]
        fn inverse_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            let mut bar = GF2_8::new(0b_0000_0010);
            assert_eq!(foo.inverse().unwrap().inner, 0x83);
            assert_eq!(bar.inverse().unwrap().inner, 0x8D);
            foo = GF2_8::new(0b_1100_0010);
            bar = GF2_8::new(0b_0010_1111);
            assert_eq!(foo.inverse().unwrap().inner, 0x2F);
            assert_eq!(bar.inverse().unwrap().inner, 0xC2);
            foo = GF2_8::new(0);
            assert_eq!(foo.inverse().unwrap_or_default().inner, 0);
        }
        #[test]
        fn div_works() {
            let mut foo = GF2_8::new(0b_1000_0000);
            let mut bar = GF2_8::new(0b_0000_0010);
            assert_eq!((foo / bar).inner, 0b_0100_0000);
            foo = GF2_8::new(0b_1100_0010);
            bar = GF2_8::new(0b_0010_1111);
            assert_eq!((foo / bar).inner, 0b_0011_0101);
            foo = GF2_8::new(0b_1010_0110);
            bar = GF2_8::new(1);
            assert_eq!((foo / bar).inner, 0b_1010_0110);
        }
        #[test]
        #[should_panic]
        fn div_zero_panic() {
            let foo = GF2_8::new(1);
            let bar = GF2_8::new(0);
            let _p = foo / bar;
        }
    }
}
mod aes_affine_mapping {
    const AES_AFFINE_MAPPING_MATRIX: [u8; 8] = [
        0b_1000_1111,
        0b_1100_0111,
        0b_1110_0011,
        0b_1111_0001,
        0b_1111_1000,
        0b_0111_1100,
        0b_0011_1110,
        0b_0001_1111,
    ];
    const AES_AFFINE_MAPPING_VECTOR: [u8; 8] = [1, 1, 0, 0, 0, 1, 1, 0];
    // This matrix isn't a part of AES standard, nether a part in the original paper.
    // Because AES standard just gave the table of inversed S-Box directly.
    // This is from the book "The design of Rijndael: AES -- the Advanced Encryption Standard".
    const AES_INVERSE_AFFINE_MAPPING_MATRIX: [u8; 8] = [
        0b_0010_0101,
        0b_1001_0010,
        0b_0100_1001,
        0b_1010_0100,
        0b_0101_0010,
        0b_0010_1001,
        0b_1001_0100,
        0b_0100_1010,
    ];
    const AES_INVERSE_AFFINE_MAPPING_VECTOR: [u8; 8] = [1, 0, 1, 0, 0, 0, 0, 0];
    macro_rules! swap_binary {
        ($input:expr) => {{
            let mut input: u8 = $input;
            let mut output: u8 = input & 0b_0000_0001;
            for _ in 1..8 {
                output <<= 1;
                input >>= 1;
                // Bitwise operator is a little faster than add operator. They achieve the same effect
                // because there is no need to carry. So I use `^=` instead of `+=` here.
                output ^= input & 0b_0000_0001;
            }
            output
        }};
    }
    macro_rules! affine_mapping_operate {
        ($value:ident, $matrix:ident, $vector:ident) => {{
            let mut result: u8 = 0;
            for i in (0..8).rev() {
                // I use `^=` instead of `+=` because there is no need to carry.
                // Also `^` for `+`.
                // For a unsigned integer, `% 2` only depends on LSB, so I use faster bitwise operator
                // rather than remainder operator.
                result ^= ((swap_binary!($matrix[i]) & $value).count_ones() as u8 ^ $vector[i])
                    & 0b_0000_0001;
                if i != 0 {
                    result <<= 1;
                }
            }
            result
        }};
    }
    pub fn aes_sbox_affine_mapping(value: u8) -> u8 {
        affine_mapping_operate!(value, AES_AFFINE_MAPPING_MATRIX, AES_AFFINE_MAPPING_VECTOR)
    }
    pub fn aes_sbox_inverse_affine_mapping(value: u8) -> u8 {
        affine_mapping_operate!(
            value,
            AES_INVERSE_AFFINE_MAPPING_MATRIX,
            AES_INVERSE_AFFINE_MAPPING_VECTOR
        )
    }
    #[cfg(test)]
    mod tests {
        use super::aes_sbox_affine_mapping as affine_mapping;
        use super::aes_sbox_inverse_affine_mapping as inverse_mapping;
        #[test]
        fn it_works() {
            for i in 0..255 {
                assert_eq!(i, inverse_mapping(affine_mapping(i)));
            }
            assert_eq!(255, inverse_mapping(affine_mapping(255)));
        }
    }
}
mod t_box {
    use super::gf28::GF2_8;
    // The matrix in MixColumn transformation is broken down into column vectors.
    const ENCRYPT_T0_VECTOR: [u8; 4] = [0x02, 0x01, 0x01, 0x03];
    const ENCRYPT_T1_VECTOR: [u8; 4] = [0x03, 0x02, 0x01, 0x01];
    const ENCRYPT_T2_VECTOR: [u8; 4] = [0x01, 0x03, 0x02, 0x01];
    const ENCRYPT_T3_VECTOR: [u8; 4] = [0x01, 0x01, 0x03, 0x02];
    const DECRYPT_T0_VECTOR: [u8; 4] = [0x0E, 0x09, 0x0D, 0x0B];
    const DECRYPT_T1_VECTOR: [u8; 4] = [0x0B, 0x0E, 0x09, 0x0D];
    const DECRYPT_T2_VECTOR: [u8; 4] = [0x0D, 0x0B, 0x0E, 0x09];
    const DECRYPT_T3_VECTOR: [u8; 4] = [0x09, 0x0D, 0x0B, 0x0E];
    macro_rules! do_the_calculation {
        ($gf:ident, $vector:ident) => {{
            let mut multiplier = GF2_8::default();
            let mut values = [0_u8; 4];
            for i in 0..4 {
                multiplier.set($vector[i]);
                values[i] = (multiplier * (*$gf)).get_byte();
            }
            ::std::primitive::u32::from_le_bytes(values)
        }};
    }
    pub fn e_t0_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, ENCRYPT_T0_VECTOR)
    }
    pub fn e_t1_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, ENCRYPT_T1_VECTOR)
    }
    pub fn e_t2_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, ENCRYPT_T2_VECTOR)
    }
    pub fn e_t3_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, ENCRYPT_T3_VECTOR)
    }
    pub fn d_t0_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, DECRYPT_T0_VECTOR)
    }
    pub fn d_t1_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, DECRYPT_T1_VECTOR)
    }
    pub fn d_t2_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, DECRYPT_T2_VECTOR)
    }
    pub fn d_t3_element(gf: &GF2_8) -> u32 {
        do_the_calculation!(gf, DECRYPT_T3_VECTOR)
    }
    #[cfg(test)]
    mod tests {
        use super::*;
        #[test]
        fn et0_works() {
            let tester = GF2_8::new(0xC2).inverse().unwrap();
            assert_eq!(e_t0_element(&tester), 0x712F2F5E);
        }
        #[test]
        fn dt0_works() {
            let tester = GF2_8::new(0x02);
            assert_eq!(d_t0_element(&tester), 0x161A121C);
        }
    }
}

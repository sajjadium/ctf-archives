use std::io;

fn check_flag(flag: &str) -> bool {
    flag.as_bytes()[18] as i32 * flag.as_bytes()[7] as i32 & flag.as_bytes()[12] as i32 ^ flag.as_bytes()[2] as i32 == 36 &&
    flag.as_bytes()[1] as i32 % flag.as_bytes()[14] as i32 - flag.as_bytes()[21] as i32 % flag.as_bytes()[15] as i32 == -3 &&
    flag.as_bytes()[10] as i32 + flag.as_bytes()[4] as i32 * flag.as_bytes()[11] as i32 - flag.as_bytes()[20] as i32 == 5141 &&
    flag.as_bytes()[19] as i32 + flag.as_bytes()[12] as i32 * flag.as_bytes()[0] as i32 ^ flag.as_bytes()[16] as i32 == 8332 &&
    flag.as_bytes()[9] as i32 ^ flag.as_bytes()[13] as i32 * flag.as_bytes()[8] as i32 & flag.as_bytes()[16] as i32 == 113 &&
    flag.as_bytes()[3] as i32 * flag.as_bytes()[17] as i32 + flag.as_bytes()[5] as i32 + flag.as_bytes()[6] as i32 == 7090 &&
    flag.as_bytes()[21] as i32 * flag.as_bytes()[2] as i32 ^ flag.as_bytes()[3] as i32 ^ flag.as_bytes()[19] as i32 == 10521 &&
    flag.as_bytes()[11] as i32 ^ flag.as_bytes()[20] as i32 * flag.as_bytes()[1] as i32 + flag.as_bytes()[6] as i32 == 6787 &&
    flag.as_bytes()[7] as i32 + flag.as_bytes()[5] as i32 - flag.as_bytes()[18] as i32 & flag.as_bytes()[9] as i32 == 96 &&
    flag.as_bytes()[12] as i32 * flag.as_bytes()[8] as i32 - flag.as_bytes()[10] as i32 + flag.as_bytes()[4] as i32 == 8277 &&
    flag.as_bytes()[16] as i32 ^ flag.as_bytes()[17] as i32 * flag.as_bytes()[13] as i32 + flag.as_bytes()[14] as i32 == 4986 &&
    flag.as_bytes()[0] as i32 * flag.as_bytes()[15] as i32 + flag.as_bytes()[3] as i32 == 7008 &&
    flag.as_bytes()[13] as i32 + flag.as_bytes()[18] as i32 * flag.as_bytes()[2] as i32 & flag.as_bytes()[5] as i32 ^ flag.as_bytes()[10] as i32 == 118 &&
    flag.as_bytes()[0] as i32 % flag.as_bytes()[12] as i32 - flag.as_bytes()[19] as i32 % flag.as_bytes()[7] as i32 == 73 &&
    flag.as_bytes()[14] as i32 + flag.as_bytes()[21] as i32 * flag.as_bytes()[16] as i32 - flag.as_bytes()[8] as i32 == 11228 &&
    flag.as_bytes()[3] as i32 + flag.as_bytes()[17] as i32 * flag.as_bytes()[9] as i32 ^ flag.as_bytes()[11] as i32 == 11686 &&
    flag.as_bytes()[15] as i32 ^ flag.as_bytes()[4] as i32 * flag.as_bytes()[20] as i32 & flag.as_bytes()[1] as i32 == 95 &&
    flag.as_bytes()[6] as i32 * flag.as_bytes()[12] as i32 + flag.as_bytes()[19] as i32 + flag.as_bytes()[2] as i32 == 8490 &&
    flag.as_bytes()[7] as i32 * flag.as_bytes()[5] as i32 ^ flag.as_bytes()[10] as i32 ^ flag.as_bytes()[0] as i32 == 6869 &&
    flag.as_bytes()[21] as i32 ^ flag.as_bytes()[13] as i32 * flag.as_bytes()[15] as i32 + flag.as_bytes()[11] as i32 == 4936 &&
    flag.as_bytes()[16] as i32 + flag.as_bytes()[20] as i32 - flag.as_bytes()[3] as i32 & flag.as_bytes()[9] as i32 == 104 &&
    flag.as_bytes()[18] as i32 * flag.as_bytes()[1] as i32 - flag.as_bytes()[4] as i32 + flag.as_bytes()[14] as i32 == 5440 &&
    flag.as_bytes()[8] as i32 ^ flag.as_bytes()[6] as i32 * flag.as_bytes()[17] as i32 + flag.as_bytes()[12] as i32 == 7104 &&
    flag.as_bytes()[11] as i32 * flag.as_bytes()[2] as i32 + flag.as_bytes()[15] as i32 == 6143
}

fn main() {
    let mut flag = String::new();
    println!("Enter the flag: ");
    io::stdin().read_line(&mut flag).expect("Failed to read line");
    let flag = flag.trim();

    if check_flag(flag) {
        println!("Correct flag");
    } else {
        println!("Wrong flag");
    }
}
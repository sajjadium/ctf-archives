use std::collections::{ HashMap, HashSet };
use std::num::ParseIntError;
use std::io::{ stdin, Stdin, Write };
use std::thread::sleep;
use std::time::{ SystemTime, UNIX_EPOCH, Duration };
// use ******* as proprietary_algorithm;
// good luck :)

static START_TEXT: &str = r#"
You're one of the first people to begin mars's colonization!
To reserve your plot of land, you may request the placement of a flag.
Stipulations and other information about the registration process can be viewed with the "info" command.

All the flag placing is done by our magical superintelligent, ultra-fast, mostly-completed Quizzicality rover.
More information about the rover can be viewed with the "rover" command.
"#;

static INFO_TEXT: &str = r#"
Your IGUID - or your InterGalactic User ID - will be used to verify all flag placements.
Due to limitations in our system, your IGUID is not checked for validity.
We blame the legacy IGUID code.
We trust that you will only enter valid and registered IGUIDs.

When you request the placement of your flag we'll write down your IGUID for anti-duplication purposes.
YOU ARE ONLY ALLOWED TO PLACE ONE FLAG PER IGUID!
FAILURE TO DO SO WILL RESULT IN TERMINATION OF YOUR BCACTF ACCOUNT! (dw im probably kidding)


After you register a flag will be placed, which will have any information you need to colonize your plot of land.

But! Due to the intergalactic time-colonization-temporal-extension-based required-wait law, you may only view it after 100 years.
"#;

static ROVER_TEXT: &str = r#"
Due to the Quizzicality rover still being in its infancy, the code is not finalized.
When placing the flag, the rover first heads to the space.
This space is designated by a "proprietary" algorithm that uses your IGUID as input and spits out the location.

There are 340282366920938463463374607431768211456 different possible outputs of the algorithm.
So we're safe.
Hopefully nothing bad happens.
That might cause some information leakage.
Oh well.
That's really unlikely.
¯\_(ツ)_/¯
"#;

static HELP_TEXT: &str = r#"
The commands are:
    "plant a flag" - Plants a flag at a specific key and locks that key.
    "check a flag" - Checks for a flag at an unlocked key.
    "help"         - Displays this message.
    "info"         - Displays more information about the process for applying to have a flag placed.
    "rover"        - Gives more information about the rover and the flag-placing process.
    "" or "exit"   - Exits the program.
"#;

static SECS_IN_100_YEARS: u64 = 25 * (365 * 3 + 366) * 24 * 60 * 60;

static PRE_REGISTERED_ACCOUNTS: [&str; 5] = [
    "c2t5", // The all-knowing, all-powerful problem writer
    "S2VhbnUgUmVldmVz", // Due to this person, I am no longer able to breathe :(
    "i2pqKIndovqHTYRzfZBItfp9K8YwrlWyQHhRnEanPYk=", // My favorite demogorgon pet
    "kFM3TReJ2zHSLDvJdvIERV7AbWYWzOVQXWqDgVX7PoAeXj3pDJuyKFTwTaz4lVtQHCG3sQRMqI0KXUk91IECODCNvaJK8PayTmiFxFe5uQlUkGFD1FLdOaaT2QBri91DLzYqPaG7POm5Buyem0YxRa6kKpMxUb1TnpAbT0a6lN8=", // The other proposed name for my bearded dragon
    "0THdAsXm7sRpPZoGmK/5XC/KtQcSRn6rQARYPrj7f4lVrTQGCfSzAoPkiIMl8UFaCFEl6PfNyZ/ZHb1ygDc8W9iCPjFWNI9brm2s1DbJGcbdU+I0h9oD/QI5YwbSSM2g6Z8zQg9XfujOVLZwgCgNHsaYIby2qIOTlvllq2/3KnA=", // The Flying Spaghetti Monster's real name
];



/// Spaghetti code lol
fn main() {
    let flag: String = get_flag();

    let mut used_iguids = HashSet::new();
    let mut plot_map = HashMap::new();

    let stdin = stdin();

    println!("{}{}", START_TEXT, HELP_TEXT);

    PRE_REGISTERED_ACCOUNTS
        .iter()
        .cloned()
        .map(base64_decode)
        .inspect(|name| println!("Pre-registering member: {}", sanitize_to_string(name)))
        .map(proprietary_algorithm)
        .for_each(|digest| {
            plot_map.insert(digest, ("flag{PREREGISTERED_DUMMY_FLAG}", UNIX_EPOCH));
        });

    loop {
        println!("Enter a command:");

        let command = get_line_stdin(&stdin);
        println!("");

        match command.as_str() {


            "plant a flag" => if used_iguids.len() < 10 {
                println!("Enter your IGUID (in hexadecimal):");

                let input = get_line_stdin(&stdin);
                match decode_hex(&input) {
                    Ok(iguid_bytes) => {
                        println!("");

                        if used_iguids.get(&input).is_none() {
                            used_iguids.insert(input.clone());
                            let hash = proprietary_algorithm(&iguid_bytes);
                            plot_map.insert(hash, (&flag, SystemTime::now()));
                            println!("Flag planted!");
                        } else {
                            eprintln!("You already used that IGUID!");
                        }
                    }
                    Err(_) => eprintln!("Please enter a valid hexadecimal string."),
                }
            } else {
                eprintln!("You can only plant up to 10 flags per instance.");
            },


            "check a flag" => {
                println!("Enter your IGUID (in hexadecimal):");

                let input = get_line_stdin(&stdin);
                match decode_hex(&input) {
                    Ok(input_string) => {
                        println!("");

                        if used_iguids.get(&input).is_none() {
                            let hash = proprietary_algorithm(&input_string);
        
                            println!(r#"Checking for flag with IGUID "{}"..."#, sanitize_to_string(&input_string));
        
                            let output = plot_map.get(&hash);
                            match output {
                                Some(flag) => unimplemented!(r#"FLAG "{:#?}" ALREADY FOUND! FATAL ERROR!"#, flag),
                                None => eprintln!(r#"No flag was found with IGUID "{}"."#, input),
                            }
                        } else {
                            let hash = proprietary_algorithm(&input_string);
                            if let Some(info) = plot_map.get(&hash) {
                                if SystemTime::now().duration_since(info.1).unwrap().as_secs() >= SECS_IN_100_YEARS {
                                    println!("YAY! YOU'RE READY TO BEGIN COLONIZATION! Here's your information:\n{:#?}", info);
                                }
                            }
                            eprintln!(r#"Less than 100 years have passed, "{}". Sorry!"#, sanitize_to_string(&input_string));
                        }
                    },

                    Err(_) => eprintln!("Please enter a valid hexadecimal string."),
                }
                
            },


            "" | "exit" => break,

            "info" => println!("{}", INFO_TEXT),
            "rover" => println!("{}", ROVER_TEXT),
            "help" => println!("{}", HELP_TEXT),


            _ => {
                eprintln!(r#"Command "{}" does not exist!"#, command);
                println!("{}", HELP_TEXT);
            },
        }
        println!("\n");
    }
    println!("Goodbye!");
}

fn get_flag() -> String {
    std
        ::env
        ::var("FLAG")
        .unwrap_or_else(
            |_| std
                    ::fs
                    ::read_to_string("flag.txt")
                    .unwrap_or("flag{dummy_flag}".into())
        )
}

fn get_line_stdin(stdin: &Stdin) -> String {
    let mut string = String::new();
    stdin.read_line(&mut string).unwrap();

    let mut string_characters = string.chars();
    string_characters.next_back();
    string_characters.as_str().to_owned()
}

pub fn decode_hex(s: &str) -> Result<Vec<u8>, ParseIntError> {
    (0..(s.len() / 2) * 2)
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16))
        .collect()
}


/// I didn't want to use a for loop. I am deeply sorry.
pub fn base64_decode(input: &str) -> Vec<u8> {
    const BASE_64_INDEX_MAP: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    input.chars().skip(0).step_by(4).zip(
        input.chars().skip(1).step_by(4).zip(
            input.chars().skip(2).step_by(4).zip(
                input.chars().skip(3).step_by(4)
            )
        )
    )
        .map(
            |(a, (b, (c, d)))| {
                let mut bit_count = 0;
                (
                    [a, b, c, d]
                        .iter()
                        .map(|chr| 
                            BASE_64_INDEX_MAP.find(*chr).map(|i| usize::to_le_bytes(i)[0])
                        )
                        .inspect(|v| if v.is_some() { bit_count += 6 })
                        .map(|optional_value| optional_value.unwrap_or(0))
                        .fold(0u32, |num, n| (num << 6) + u32::from(n)),
                    bit_count
                )
            }
        )
        .map(|(int, bit_count)| (u32::to_be_bytes(int), bit_count))
        .map(|(bytes, bit_count)| bytes.iter().take(bit_count).cloned().collect::<Vec<_>>())
        .flatten()
        .collect()
}

fn sanitize_to_string<'a>(input: impl IntoIterator<Item = &'a u8>) -> String {
    String::from_utf8_lossy(&input.into_iter().cloned().filter(|byte| !char::is_ascii_control(&(*byte as char))).collect::<Vec<_>>()).to_string()
}
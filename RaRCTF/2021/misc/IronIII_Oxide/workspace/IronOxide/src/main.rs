use std::fs::File;
use std::error::{Error};
use std::io::{self, Write, Read};
use std::process;
use serde::Deserialize;
use rand::{thread_rng, Rng};
use std::str;
// DISCLAIMER: Chemical processes replicated in the program are simplified and not extremely accurate
#[derive(Debug)]
struct Atom<'a> {
    element: Element,
    bonds: Vec<Bond<'a>>
}
impl Atom<'_> {
    fn from_element(element: &Element) -> Atom {
        Atom {
            element: element.clone(),
            bonds: Vec::<Bond>::new(),

        }
    }
    fn from_symbol<'a>(symbol: &str, elements: &'a Vec<Element>) -> Option<Atom<'a>> {
        for element in elements.iter() {
            if element.symbol == symbol {
                return Some(Atom::from_element(element));
            }
        }
        None
    }
    fn from_atomic_number<'a>(number: u8, elements: &'a Vec<Element>) -> Option<Atom<'a>> {
        for element in elements.iter() {
            if element.atomicnumber == number {
                return Some(Atom::from_element(element));
            }
        }
        None
    }
}
#[derive(Debug, Clone, Deserialize)]
struct Element {
    atomicnumber: u8,
    symbol: String,
    valence: i8,
    electronegativity: f64,
    group: u8,
    period: u8
}
#[derive(Debug)]
struct Bond<'b> {
    bondtype: BondType,
    atoms: [&'b Atom<'b>; 2]
}

impl Bond<'_> {
    fn new<'b>(atom1: &'b Atom, atom2: &'b Atom) -> Option<Bond<'b>>{
        let bondtype;
        if atom1.element.valence == 0 || atom2.element.valence == 0 {
            // Noble gas bonds not implemented
            return None;
        }
        else if atom1.element.valence.signum() != atom2.element.valence.signum() {
            // Ionic
            bondtype = BondType::Ionic;
        }
        else if atom1.element.valence.signum() == 1 && atom2.element.valence.signum() == 1 {
            // Metallic
            bondtype = BondType::Metallic;
        }
        else {
            // Covalent
            bondtype = BondType::Covalent;
        }
        Some(Bond {
            bondtype,
            atoms: [atom1, atom2]
        })

    }
}
#[derive(Debug)]
enum BondType {
    Covalent,
    Ionic,
    Metallic
}

fn main() -> Result<(), Box<dyn Error>>  {
    let mut elements = Vec::<Element>::new();
    let response = fill_elements(&mut elements);
    if let Err(err) = response {
        println!("Error parsing CSV: {}", err);
        process::exit(1);
    }
    // Generate lab key using secure RNG
    println!("Generating lab key...");
    let mut rng = thread_rng();
    let mut lab_key = [0u8; 25];
    for i in 0..25 {
        lab_key[i] = rng.gen_range(65..127);
    }
    let lab_key = str::from_utf8(&lab_key[..]).unwrap();
    let chem_password: Vec<Atom> = lab_key.as_bytes().iter().map(|x| Atom::from_atomic_number(*x - 64, &elements).unwrap()).collect();
    println!("Doing experiment...");
    for i in 0..25 {
        for j in 0..25 {
            // Reactions with two of the same element are counterproductive
            if i == j {
                continue;
            }
            // Give results of reaction, this should be more than enough
            let first = &chem_password[i];
            let second = &chem_password[j];
            let difference1 = (first.element.atomicnumber as i16 - second.element.atomicnumber as i16).abs();
            let difference2 = (first.element.electronegativity - second.element.electronegativity).abs();
            let bond = Bond::new(first, second);
            match bond {
                Some(thebond) => println!("Results for index {} and {}: {:?}, {}, {:.2}", i, j, thebond.bondtype, difference1, difference2),
                None => println!("Results for index {} and {}: {}, {}, {:.2}", i, j, "No Reaction", difference1, difference2),
            }
        }
    }
    for _ in 0..100 {
        let mut attempt = String::new();
        print!("Enter your lab key: ");
        io::stdout().flush(); // It won't error :)
        io::stdin()
            .read_line(&mut attempt)
            .unwrap();
        if attempt.trim() == lab_key.to_owned() {
            print_flag()?;
            process::exit(0);
        }
        else {
            println!("Insert chemistry joke here(your password is wrong btw)");
        }
    }
    Ok(())
}
// This isn't copied and repurposed from the rust docs, I promise
fn fill_elements(elemvec: &mut Vec<Element>) -> Result<(), Box<dyn Error>> {
     let elemfile = File::open("elemprops.csv").expect("Failed to open file");
     let mut elemrdr = csv::Reader::from_reader(elemfile);
     for result in elemrdr.deserialize() {
         let mut record: Element = result?;
         // 0 is a placeholder for places where electronegativity isn't applicable
         if record.electronegativity == 0.0 {
             record.electronegativity = f64::NAN;
         }
         elemvec.push(record);
     }
     Ok(())
}
fn print_flag() -> Result<(), Box<dyn Error>>  {
    let mut flag = String::new();
    let mut flagfile = File::open("flag.txt")?;
    flagfile.read_to_string(&mut flag)?;
    println!("Flag: {}",flag);
    Ok(())
}
use clap::Parser;
use image::DynamicImage;
use image::io::Reader as ImageReader;
use itertools::Itertools;
use pbr::Pipe;
use std::net::TcpStream;

use fancy_garbling::twopac::semihonest::Evaluator;
use fancy_garbling::util as numbers;
use fancy_garbling::{AllWire, CrtGadgets, Fancy, FancyInput};
use ocelot::ot::AlszReceiver;
use scuttlebutt::AesRng;
use scuttlebutt::{AbstractChannel, SymChannel};

use dicenet::layer::Accuracy;
use dicenet::neural_net::NeuralNet;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    address: String,

    #[arg(long)]
    file: String,

    #[arg(long)]
    model: String,

    // use the dummy weights file
    #[arg(long)]
    weights: String,
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();

    let img = ImageReader::open(args.file)?.decode().expect("bad file");
    let pixels: Vec<u128> = if let DynamicImage::ImageLuma8(img) = img {
        assert!(img.width() == 64 && img.height() == 64, "image must be 64x64");
        img.into_raw().iter().map(|&x| x.into()).collect()
    } else {
        panic!("image must be 8-bit Luma");
    };

    let nn = NeuralNet::from_json(&args.model, &args.weights);
    let accuracy = Accuracy {
        relu: "100%".to_string(),
        sign: "100%".to_string(),
        max: "100%".to_string(),
    };
    let bitwidths = vec![15; nn.nlayers() + 1];
    let moduli = bitwidths
        .iter()
        .map(|&b| numbers::modulus_with_width(b as u32))
        .collect_vec();

    let stream = TcpStream::connect(args.address)?;
    let mut channel = SymChannel::new(stream);
    let mut magic = [0; 8];
    channel.read_bytes(&mut magic).unwrap();
    assert_eq!(b"DICENET\n", &magic);
    let mut ev = Evaluator::<_, _, AlszReceiver, AllWire>::new(channel, AesRng::new()).unwrap();
    let inputs = ev.crt_encode_many(&pixels, moduli[0]).unwrap();
    let scores =
        nn.eval_arith::<_, _, Pipe>(&mut ev, &inputs, &moduli, None, 0, true, false, &accuracy);
    let bit = ev.crt_geq(&scores[0], &scores[1], &accuracy.sign).unwrap();
    let is_flag = ev.output(&bit).unwrap();
    
    if let Some(1) = is_flag {
        println!("yup, that's the flag!");
    } else {
        println!("nope");
    }

    Ok(())
}

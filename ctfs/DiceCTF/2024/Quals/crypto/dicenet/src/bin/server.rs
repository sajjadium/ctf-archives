use clap::Parser;
use itertools::Itertools;
use pbr::Pipe;
use std::io;
use std::net::TcpListener;

use fancy_garbling::twopac::semihonest::Garbler;
use fancy_garbling::util as numbers;
use fancy_garbling::{AllWire, CrtGadgets, Fancy, FancyInput};
use ocelot::ot::AlszSender;
use scuttlebutt::AesRng;
use scuttlebutt::{AbstractChannel, Channel, SymChannel};

use dicenet::layer::Accuracy;
use dicenet::neural_net::NeuralNet;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    address: Option<String>,

    #[arg(long)]
    model: String,

    #[arg(long)]
    weights: String,
}

fn handle<C: AbstractChannel>(mut channel: C, nn: &NeuralNet, moduli: &[u128], accuracy: &Accuracy) {
    channel.write_bytes(b"DICENET\n").unwrap();
    let mut gb = Garbler::<_, _, AlszSender, AllWire>::new(channel, AesRng::new()).unwrap();
    let inputs = gb.crt_receive_many(nn.num_inputs(), moduli[0]).unwrap();
    let scores =
        nn.eval_arith::<_, _, Pipe>(&mut gb, &inputs, &moduli, None, 0, true, true, &accuracy);
    // gb.crt_outputs(&scores).unwrap();
    let bit = gb.crt_geq(&scores[0], &scores[1], &accuracy.sign).unwrap();
    gb.output(&bit).unwrap();
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();

    let nn = NeuralNet::from_json(&args.model, &args.weights);

    let bitwidths = vec![15; nn.nlayers() + 1];
    let moduli = bitwidths
        .iter()
        .map(|&b| numbers::modulus_with_width(b as u32))
        .collect_vec();

    let accuracy = Accuracy {
        relu: "100%".to_string(),
        sign: "100%".to_string(),
        max: "100%".to_string(),
    };

    if let Some(address) = args.address {
        let listener = TcpListener::bind(address)?;
        for stream in listener.incoming() {
            let channel = SymChannel::new(stream?);
            handle(channel, &nn, &moduli, &accuracy);
        }
    } else {
        let channel = Channel::new(io::stdin(), io::stdout());
        handle(channel, &nn, &moduli, &accuracy);
    }

    Ok(())
}

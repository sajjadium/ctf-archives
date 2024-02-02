use crate::layer::{Accuracy, Layer};
use colored::*;
use fancy_garbling::{
    BinaryBundle, CrtBundle, Fancy, FancyArithmetic, FancyBinary, FancyInput, HasModulus,
};
use itertools::Itertools;
use ndarray::Array3;
use pbr::ProgressBar;
use serde_json::{self, Value};
use std::fs::File;

/// The neural network struct
#[derive(Clone)]
pub struct NeuralNet {
    layers: Vec<Layer>,
}

impl NeuralNet {
    /// Get the number of inputs to the first layer.
    pub fn num_inputs(&self) -> usize {
        self.layers[0].input_size()
    }

    /// Print info about the neural network.
    pub fn print_info(&self) {
        println!("{}", "neural net info:".yellow());
        println!("  input dimensions: {:?}", self.layers[0].input_dims());
        for layer in self.layers.iter() {
            println!("  {}", layer.info());
            println!("    inp={:?}", layer.input_dims());
            println!("    out={:?}", layer.output_dims());
        }
    }

    pub fn nlayers(&self) -> usize {
        self.layers.len()
    }

    /// Convert the neural network into an arithmetic fancy computation.
    pub fn eval_arith<W, F, T>(
        &self,
        b: &mut F,
        circuit_inputs: &[CrtBundle<W>],
        moduli: &[u128], // CRT moduli for each layer's operations
        mut pb: Option<&mut ProgressBar<T>>,
        max_threads: usize,
        secret_weights: bool,
        secret_weights_owned: bool,
        accuracy: &Accuracy,
    ) -> Vec<CrtBundle<W>>
    where
        W: HasModulus + Clone,
        F: Fancy<Item = W> + FancyInput<Item = W> + FancyArithmetic + FancyBinary,
        T: std::io::Write,
    {
        assert_eq!(
            moduli.len(),
            self.nlayers() + 1,
            "moduli for each layer and output required"
        );

        // set the progress bar to 0
        pb.as_mut().map(|pb| pb.set(0));

        // each layers input/output
        let mut acc =
            Array3::from_shape_vec(self.layers[0].input_dims(), circuit_inputs.to_vec()).unwrap();

        for (i, layer) in self.layers.iter().enumerate() {
            // update the progress bar
            pb.as_mut().map(|pb| {
                pb.message(&format!("Layer [{}] ", layer.name()));
                pb.inc();
            });

            // evaluate this layer as fancy
            let inp_mod = moduli[i];
            let out_mod = moduli[i + 1];
            acc = layer.as_arith(
                b,
                inp_mod,
                out_mod,
                &acc,
                max_threads,
                secret_weights,
                secret_weights_owned,
                accuracy,
            );
        }

        acc.into_iter().cloned().collect_vec()
    }

    /// Evaluate the neural network as boolean fancy computation.
    pub fn eval_boolean<W, F, T>(
        &self,
        b: &mut F,
        circuit_inputs: &[BinaryBundle<W>],
        bitwidth: &[usize],
        mut pb: Option<&mut ProgressBar<T>>,
        max_threads: usize,
        secret_weights: bool,
        secret_weights_owned: bool,
    ) -> Vec<BinaryBundle<W>>
    where
        W: Clone + HasModulus,
        F: Fancy<Item = W> + FancyInput<Item = W> + FancyArithmetic + FancyBinary,
        T: std::io::Write,
    {
        let mut acc =
            Array3::from_shape_vec(self.layers[0].input_dims(), circuit_inputs.to_vec()).unwrap();
        pb.as_mut().map(|pb| pb.set(0));
        for (i, layer) in self.layers.iter().enumerate() {
            pb.as_mut().map(|pb| {
                pb.message(&format!("Layer [{}] ", layer.name()));
                pb.inc();
            });
            acc = layer.as_binary(
                b,
                bitwidth[i],
                bitwidth[i + 1],
                &acc,
                max_threads,
                secret_weights,
                secret_weights_owned,
            );
        }
        acc.iter().cloned().collect_vec()
    }

    /// Find max/min number of bits necessary for a value on any wire in the neural network by layer.
    pub fn max_bitwidth(&self, inputs: &[Array3<i64>]) -> Vec<f64> {
        let mut pb = pbr::ProgressBar::new(inputs.len() as u64);
        let mut max_nbits: Vec<f64> = vec![0.0; self.layers.len()];

        for input in inputs.iter() {
            pb.message(&format!(
                "Computing bitwidth: [{}] ",
                itertools::join(max_nbits.iter().map(|nbits| format!("{:.0}", nbits)), ", ")
            ));
            pb.inc();

            let mut input = input.clone();
            for (j, layer) in self.layers.iter().enumerate() {
                let (output, new_max_val) = layer.max_bitwidth(&input, 8);

                let nbits = if new_max_val < 0 {
                    1.0 + ((-new_max_val) as f64).log2().ceil()
                } else {
                    (new_max_val as f64).log2().ceil()
                };

                if nbits > max_nbits[j] {
                    max_nbits[j] = nbits;
                }

                input = output;
            }
        }

        pb.finish();
        max_nbits
    }

    /// Evaluate the neural network over `i64` values.
    pub fn eval_plaintext(&self, input: &Array3<i64>) -> Array3<i64> {
        self.layers
            .iter()
            .fold(input.clone(), |acc, layer| layer.as_plaintext(&acc, 32))
    }

    ////////////////////////////////////////////////////////////////////////////////
    // io

    /// Read a neural network from the tensorflow JSON output.
    pub fn from_json(model_filename: &str, weights_filename: &str) -> Self {
        let file = File::open(model_filename)
            .unwrap_or_else(|_| panic!("couldn't open file: {}", model_filename));
        let obj: Value = serde_json::from_reader(file).expect("couldn't parse json!");
        let obj = obj
            .as_object()
            .expect("root value in model.json is not an object");
        let layers_obj = if obj["config"].is_array() {
            &obj["config"]
        } else {
            &obj["config"]
                .as_object()
                .expect("base config is not an object!")["layers"]
        };
        let layer_objs = layers_obj
            .as_array()
            .expect("layers is not an array")
            .into_iter()
            .map(|c| c.as_object().unwrap());

        let file = File::open(weights_filename).expect("couldn't open file!");
        let obj: Value = serde_json::from_reader(file).expect("couldn't parse json!");
        let mut weights_iter = obj.as_array().unwrap().chunks(2);

        let mut layers: Vec<Layer> = Vec::new();

        for (_i, layer) in layer_objs.enumerate() {
            // println!("reading {}", layer["class_name"].as_str().unwrap());
            // for l in layers.iter() {
            //      println!("{} output_shape={:?}", l.info(), l.output_dims());
            // }
            // println!();

            let cfg = layer["config"].as_object().unwrap();
            let input_shape = input_shape(&cfg, &layers);

            match layer["class_name"].as_str().unwrap().as_ref() {
                "Dense" => {
                    let weights_and_biases =
                        weights_iter.next().expect("not enough weights and biases!");
                    let num_neurons = cfg["units"].as_u64().unwrap() as usize;
                    let mut weights = vec![Array3::from_elem(input_shape, Some(0)); num_neurons];

                    // keras outputs the weights in the transposition of what we need
                    let data_arr = weights_and_biases[0].as_array().unwrap();
                    assert_eq!(data_arr.len(), input_shape.0);

                    let data = data_arr.into_iter().map(|v| {
                        v.as_array()
                            .unwrap_or_else(|| panic!("not an array: {}", v))
                            .into_iter()
                            .map(|v| {
                                v.as_i64()
                                    .unwrap_or_else(|| panic!("non-integer in weights.json: {}", v))
                            })
                    });

                    for (inp_num, data_iter) in data.enumerate() {
                        for (neuron_num, val) in data_iter.enumerate() {
                            weights[neuron_num][(inp_num, 0, 0)] = Some(val);
                        }
                    }

                    let activation = map_activation(cfg["activation"].as_str().unwrap());
                    let biases = weights_and_biases[1]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|n| Some(n.as_i64().unwrap()))
                        .collect_vec();
                    layers.push(Layer::Dense {
                        weights,
                        biases,
                        activation,
                    });
                }

                "Dropout" => continue,

                "Conv2D" => {
                    let padding = cfg["padding"].as_str().unwrap();
                    let pad = padding == "same";

                    let activation = map_activation(cfg["activation"].as_str().unwrap());
                    let weights_and_biases =
                        weights_iter.next().expect("not enough weights and biases!");

                    let kernel_size = cfg["kernel_size"]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|v| v.as_i64().unwrap() as usize)
                        .collect_vec();
                    let kernel_shape = (kernel_size[0], kernel_size[1], input_shape.2);

                    let stride = cfg["strides"]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|v| v.as_i64().unwrap() as usize)
                        .collect_vec();
                    let stride = (stride[0], stride[1]);

                    let weights = weights_and_biases[0]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|v| {
                            v.as_array()
                                .unwrap()
                                .into_iter()
                                .map(|v| {
                                    v.as_array()
                                        .unwrap()
                                        .into_iter()
                                        .map(|v| {
                                            v.as_array()
                                                .unwrap()
                                                .into_iter()
                                                .map(|v| {
                                                    v.as_i64().unwrap_or_else(|| {
                                                        panic!(
                                                            "reading weights: {} not an integer",
                                                            v
                                                        )
                                                    })
                                                })
                                                .collect_vec()
                                        })
                                        .collect_vec()
                                })
                                .collect_vec()
                        })
                        .collect_vec();

                    let nfilters = cfg["filters"].as_u64().unwrap() as usize;
                    let mut filters = vec![Array3::from_elem(kernel_shape, Some(0)); nfilters];

                    assert_eq!(weights.len(), kernel_shape.0);

                    for (x, weights) in weights.into_iter().enumerate() {
                        assert_eq!(weights.len(), kernel_shape.1);

                        for (y, weights) in weights.into_iter().enumerate() {
                            assert_eq!(weights.len(), kernel_shape.2);

                            for (z, weights) in weights.into_iter().enumerate() {
                                assert_eq!(weights.len(), nfilters);

                                for (filter_num, val) in weights.into_iter().enumerate() {
                                    filters[filter_num][(x, y, z)] = Some(val);
                                }
                            }
                        }
                    }

                    let biases = weights_and_biases[1]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|n| Some(n.as_i64().unwrap()))
                        .collect_vec();

                    assert_eq!(biases.len(), nfilters);

                    layers.push(Layer::Convolutional {
                        filters,
                        biases,
                        input_shape,
                        kernel_shape,
                        stride,
                        activation,
                        pad,
                    });
                }

                "MaxPooling2D" => {
                    let padding = cfg["padding"].as_str().unwrap();

                    let pad = padding == "same";

                    let stride = cfg["strides"]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|v| v.as_i64().unwrap() as usize)
                        .collect_vec();
                    let stride = (stride[0], stride[1]);

                    let size = cfg["pool_size"]
                        .as_array()
                        .unwrap()
                        .into_iter()
                        .map(|v| v.as_i64().unwrap() as usize)
                        .collect_vec();
                    let size = (size[0], size[1]);

                    layers.push(Layer::MaxPooling2D {
                        input_shape,
                        stride,
                        size,
                        pad,
                    });
                }

                "Flatten" => {
                    let (height, width, depth) = input_shape;

                    layers.push(Layer::Flatten {
                        input_shape,
                        output_shape: (height * width * depth, 1, 1),
                    });
                }

                "Activation" => {
                    let activation = map_activation(cfg["activation"].as_str().unwrap());
                    layers.push(Layer::Activation {
                        input_shape,
                        activation,
                    });
                }

                ty => panic!("unsupported layer type \"{}\"", ty),
            }
        }

        NeuralNet { layers }
    }
}

/// Map the tensorflow activation functions to ones we support.
fn map_activation(act: &str) -> String {
    match act {
        "tanh" => "sign",
        "softmax" => "id",
        "linear" => "id",
        "relu" => "relu",
        "hard_sigmoid" => "sign",
        _ => panic!("unsupported activation: {}", act),
    }
    .to_string()
}

/// Extract the input shape from a JSON value.
fn input_shape(
    cfg: &serde_json::map::Map<String, Value>,
    layers: &[Layer],
) -> (usize, usize, usize) {
    // input_shape is the target shape for each weights array
    if let Some(v) = cfg.get("batch_input_shape") {
        let mut shape = v.as_array().unwrap().clone();
        if shape[0].is_null() {
            shape.remove(0);
        }
        let height = shape[0].as_u64().unwrap() as usize;
        let width = if shape.len() > 1 {
            shape[1].as_u64().unwrap() as usize
        } else {
            1
        };
        let depth = if shape.len() > 2 {
            shape[2].as_u64().unwrap() as usize
        } else {
            1
        };
        (height, width, depth)
    } else {
        layers.last().expect("no previous layer!").output_dims()
    }
}

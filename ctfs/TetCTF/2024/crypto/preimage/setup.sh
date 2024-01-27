#!/bin/bash
set -e

# download circom executable and trusted ptau file
mkdir downloads
wget https://github.com/iden3/circom/releases/latest/download/circom-linux-amd64 -O downloads/circom
wget https://storage.googleapis.com/zkevm/ptau/powersOfTau28_hez_final_12.ptau -O downloads/ptau12
chmod a+x downloads/circom

# install node dependencies
npm install

# compile the circuit
mkdir build
./downloads/circom circuit.circom --wasm --r1cs --sym -o build

# 2nd phase of PLONK setup
npx snarkjs plonk setup build/circuit.r1cs downloads/ptau12 build/circuit_final.zkey
npx snarkjs zkey export verificationkey build/circuit_final.zkey build/verification_key.json

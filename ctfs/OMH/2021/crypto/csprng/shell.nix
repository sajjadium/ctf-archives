{ pkgs ? import <nixpkgs> {} }:

with pkgs; mkShell {
  buildInputs = [ (secp256k1.override {
    enableECDH = true;
  }) ];
}

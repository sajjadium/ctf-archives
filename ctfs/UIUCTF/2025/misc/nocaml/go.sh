#!/bin/bash

tmp_dir=$(mktemp -d /tmp/ocaml_XXXXXX)

cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT

read -r line && echo "$line" | base64 -d > "$tmp_dir/code.ml"
ocamlc -o "$tmp_dir/out" -open Nocaml "$tmp_dir/code.ml" && "$tmp_dir/out"

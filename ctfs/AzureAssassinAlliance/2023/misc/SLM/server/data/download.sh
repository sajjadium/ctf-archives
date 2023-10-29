#!/bin/bash

if ! test -f ./data/tokenizer.json; then
    wget https://raw.githubusercontent.com/BlinkDL/ChatRWKV/main/20B_tokenizer.json tokenizer.json
fi

if ! test -f ./data/model.pth; then
    wget https://huggingface.co/BlinkDL/rwkv-4-raven/resolve/main/RWKV-4-Raven-1B5-v12-Eng98%25-Other2%25-20230520-ctx4096.pth
fi

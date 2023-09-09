#!/bin/sh
export PATH="$PATH:/usr/local/bin"
tmpfile="$(mktemp /tmp/lisp-input.XXXXXX)"
echo "Welcome to Lisp.js v0.1.0!"
echo "Input your Lisp code below and I will run it."
while true; do
  printf "> "
  read -r line
  if [ "$line" = "" ]; then
    break
  fi
  echo "$line" >> "$tmpfile"
done
node --disallow-code-generation-from-strings --disable-proto=delete main.js "$tmpfile"
rm "$tmpfile"

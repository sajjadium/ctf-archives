Welcome to pure functional madness! This challenge may be a bit different from what you're used to. But don't worry, it's just a simple crackme ;) Oh, did I mention that it's written in Nix? Good luck!

The challenge needs more stack than some distros provide and more than Nix allows by default, it should work with the following command!

docker run --rm -it --ulimit stack=2147483648:2147483648 -v "$(pwd)/crackme.nix:/crackme.nix" nixos/nix:2.26.1 \
  bash -c "nix-instantiate --option max-call-depth 1000000000 --eval /crackme.nix --argstr flag '<flag_here>'"

    the flag format is dach2025{...}

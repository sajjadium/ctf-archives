# syntax = ghcr.io/akihirosuda/buildkit-nix:v0.0.2@sha256:ad13161464806242fd69dbf520bd70a15211b557d37f61178a4bf8e1fd39f1f2

{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  outputs = { self, nixpkgs, flake-utils }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      app = pkgs.buildGoModule {
        name = "app";
        src = ./.;
        vendorSha256 = "sha256-KWpXuFmlgvaOM0kUA+3D6y8dm7llJRXMCxcb3L1dsiI=";
      };
    in rec {
      packages.${system}.app = app;
      defaultPackage.${system} = pkgs.dockerTools.buildLayeredImage {
        name = "app";
        tag = "latest";
        contents = [ app ];
        config = {
          Cmd = [ "/bin/app" ];
          ExposedPorts = { "80/tcp" = { }; };
        };
      };
    };
}
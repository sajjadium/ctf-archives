{
  description = "ctf chal";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    microvm = {
      url = "github:lf-/microvm.nix/jade/remove-linux-dev";
      # url = "github:astro/microvm.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix2container = {
      url = "github:nlewo/nix2container";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, nixpkgs, microvm, nix2container, ... }: {
    nixosConfigurations.boxMicro = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        microvm.nixosModules.microvm
        ./micro.nix
        ./flakey-ci.nix
        ({ config, pkgs, ... }: {
          microvm.qemu.extraArgs = [ "-fw_cfg" "name=flag,string=${builtins.readFile ./flag.txt}" ];
        })
      ];
    };

    devShells.x86_64-linux =
      let
        pkgs = import nixpkgs { system = "x86_64-linux"; };
      in
      {
        default = pkgs.mkShell {
          packages = with pkgs; [
            nixos-rebuild
          ];
        };
      };

    packages.x86_64-linux =
      let
        cfg' = self.nixosConfigurations.boxMicro;
        cfg = cfg'.config;
        runner = cfg.microvm.declaredRunner;
        pkgs = cfg'._module.args.pkgs;
      in
      {
        default = runner;
        dockerImage =
          let
            n2c = nix2container.packages.x86_64-linux.nix2container;
            startScript = pkgs.writeShellScript "start.sh" ''
              ${runner}/bin/microvm-run
            '';
          in
          n2c.buildImage {
            name = "flakey-ci";
            tag = "latest";

            copyToRoot = [
              (pkgs.buildEnv {
                name = "image-root";
                paths = [ pkgs.bash pkgs.coreutils ];
                pathsToLink = [ "/bin" ];
              })
            ];

            layers =
              let
                layer1 = n2c.buildLayer {
                  deps = [
                    pkgs.qemu_kvm
                  ];
                };
                layer2 = n2c.buildLayer {
                  layers = [ layer1 ];
                  deps = [
                    pkgs.systemd
                  ];
                };
                layer3 = n2c.buildLayer {
                  layers = [ layer2 ];
                  deps = [
                    cfg.microvm.kernel
                  ];
                };
                layer4 = n2c.buildLayer {
                  layers = [ layer3 ];
                  deps = [
                    pkgs.git
                  ];
                };
                layer5 = n2c.buildLayer {
                  layers = [ layer4 ];
                  deps = [
                    pkgs.nix
                    pkgs.python3
                  ];
                };
              in
              [
                layer1
                layer2
                layer3
                layer4
                layer5
              ];

            maxLayers = 50;
            config = {
              Entrypoint = [ startScript ];
              ExposedPorts = {
                "1337/tcp" = { };
              };
              Env = [ ];
            };
          };
      };
  };

}

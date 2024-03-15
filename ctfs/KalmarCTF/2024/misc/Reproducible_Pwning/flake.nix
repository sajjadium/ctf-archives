{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";
    microvm.url = "github:astro/microvm.nix";
    microvm.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} ({
      self,
      lib,
      ...
    }: let
      pkgs = inputs.nixpkgs.legacyPackages.x86_64-linux;
      imageDrv =
        pkgs.runCommand "flag-store" {
          nativeBuildInputs = [pkgs.erofs-utils];
        } (throw "secret");
    in {
      systems = ["x86_64-linux"];

      flake.nixosConfigurations = let
        modulesPath = "${inputs.nixpkgs}/nixos/modules";
        baseChall = inputs.nixpkgs.lib.nixosSystem {
          modules = [
            ({pkgs, ...}: {
              nixpkgs.hostPlatform = "x86_64-linux";
              nixpkgs.overlays = [
                (final: prev: {
                  nix = final.nixVersions.nix_2_13.overrideAttrs {
                    patches = [./nix.patch];
                    doInstallCheck = false;
                  };
                })
              ];
              environment.etc."systemd/pstore.conf".text = ''
                [PStore]
                Unlink=no
              '';

              security = {
                sudo.enable = false;
                polkit.enable = false;
              };

              users.users.root.initialHashedPassword = "x";
              users.users.user = {
                isNormalUser = true;
                initialHashedPassword = "";
                group = "user";
              };
              users.groups.user = {};

              system.stateVersion = "22.04";

              services.openssh = {
                enable = true;
                settings.PermitRootLogin = "no";
              };

              environment.noXlibs = true;
              documentation.man.enable = false;
              documentation.doc.enable = false;
              fonts.fontconfig.enable = false;

              nix.settings = {
                allow-import-from-derivation = false;
                experimental-features = ["flakes" "nix-command" "repl-flake" "no-url-literals"];
              };
              systemd.services.nix-daemon.serviceConfig.EnvironmentFile = let
                sandbox = pkgs.writeText "nix-daemon-config" ''
                  extra-sandbox-paths = /tmp/daemon=/nix/var/nix/daemon-socket/socket
                '';
                buildug = pkgs.writeText "nix-daemon-config" ''
                  build-users-group =
                '';
              in
                pkgs.writeText "env" ''
                  NIX_USER_CONF_FILES=${sandbox}:${buildug}
                '';
            })
          ];
        };
      in {
        firecracker = baseChall.extendModules {
          modules = [
            inputs.microvm.nixosModules.microvm
            (throw "secret")
          ];
        };

        iso = baseChall.extendModules {
          modules = [
            "${modulesPath}/installer/cd-dvd/iso-image.nix"
            "${modulesPath}/profiles/qemu-guest.nix"
            ({
              pkgs,
              options,
              ...
            }: {
              console.packages = options.console.packages.default ++ [pkgs.terminus_font];
              isoImage = {
                makeEfiBootable = true;
                makeUsbBootable = true;
                contents = [
                  {
                    source = pkgs.writeText "flag" "kalmar{faker_flag}";
                    target = "/flag";
                  }
                ];
              };

              # NOT part of the challenge, only to make it as close to remote as possible
              boot.postBootCommands = ''
                mkdir /data
                mount -t tmpfs -o mode=0777,rw data /data
                cp /iso/flag /data/flag
                chown -R root:root /data
                chmod 500 /data
                chmod 400 /data/flag
                mount -o remount,mode=0500,ro /data
                cp /iso/nix-store.squashfs /tmp
                umount /nix/.ro-store
                mount -t squashfs -o loop /tmp/nix-store.squashfs /nix/.ro-store
                /bin/sh -c "sleep 10; umount -fl /iso" &
                disown
              '';
            })
          ];
        };
      };

      flake.packages.x86_64-linux = {
        firecracker-conf = self.nixosConfigurations.firecracker.config.microvm.declaredRunner;
        flag-disk = imageDrv;
        iso = self.nixosConfigurations.iso.config.system.build.isoImage;
      };

      perSystem = {pkgs, ...}: {formatter = pkgs.alejandra;};
    });
}

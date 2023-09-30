{ pkgs, config, lib, ... }:
{
  networking.hostName = "micro";
  boot.initrd.systemd.enable = true;

  services.openssh.enable = true;
  users.users.root.openssh.authorizedKeys.keys = [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNldAg4t13/i69TD786The+U3wbiNUdW2Kc9KNWvEhgpf4y4x4Sft0oYfkPw5cjX4H3APqfD+b7ItAG0GCbwHw6KMYPoVMNK08zBMJUqt1XExbqGeFLqBaeqDsmEAYXJRbjMTAorpOCtgQdoCKK/DvZ51zUWXxT8UBNHSl19Ryv5Ry5VVdbAE35rqs57DQ9+ma6htXnsBEmmnC+1Zv1FE956m/OpBTId50mor7nS2FguAtPZnDPpTd5zl9kZmJEuWCrmy6iinw5V4Uy1mLeZkQv+/FtozbyifCRCvps9nHpv4mBSU5ABLgnRRvXs+D41Jx7xloNADr1nNgpsNrYaTh hed-bot-ssh-tpm-rsa"
  ];
  microvm = {
    hypervisor = "qemu";
    mem = 1024;
    interfaces = [{
      type = "user";
      id = "microvm";
      mac = "02:00:00:00:00:01";
    }];

    writableStoreOverlay = "/nix/.rw-store";
    shares = [{
      tag = "ro-store";
      source = "/nix/store";
      mountPoint = "/nix/.ro-store";
    }];
    forwardPorts = [
      {
        from = "host";
        guest.port = 1337;
        host.port = 1337;
        proto = "tcp";
      }
      {
        from = "host";
        guest.port = 22;
        host.port = 2022;
        proto = "tcp";
      }
    ];
    volumes = [
      {
        image = "guest-nix-store.img";
        mountPoint = config.microvm.writableStoreOverlay;
        size = 16384;
      }
      {
        image = "git-cache.img";
        mountPoint = "/var/lib/flakey-ci";
        size = 2048;
      }
    ];
  };
  environment.systemPackages = with pkgs; [
    tcpdump
  ];
  systemd.services.systemd-networkd = {
    environment.SYSTEMD_LOG_LEVEL = "debug";
  };
  networking.useNetworkd = true;
  system.stateVersion = "23.11";

  # it doesnt work
  systemd.services.systemd-networkd-wait-online.enable = lib.mkForce false;

  environment.noXlibs = true;

  documentation.enable = false;

  # we dont need that shit
  nixpkgs.overlays = [
    (self: super: {
      qemu_kvm = (super.qemu_kvm.override {
        nixosTestRunner = true;
        hostCpuTargets = [ "${pkgs.stdenv.hostPlatform.qemuArch}-softmmu" ];
        enableDocs = false;
      }).overrideAttrs (old: {
        postFixup = ''
          ${old.postFixup or ""}
          # save about 200mb of closure size lol
          rm $out/share/qemu/edk2-arm-*
        '';
      });
    })
  ];
}

{ pkgs, lib, ... }: {
  users.users.flakey-ci = {
    group = "flakey-ci";
    isSystemUser = true;
    home = "/var/lib/flakey-ci";
    createHome = true;
  };

  users.groups.flakey-ci = { };

  networking.firewall.allowedTCPPorts = [ 1337 ];

  nix.settings.extra-experimental-features = "nix-command flakes";
  nix.settings.trusted-users = [ "flakey-ci" ];

  systemd.services.flakey-ci = {
    path = [ pkgs.nix pkgs.git ];
    serviceConfig = {
      User = "flakey-ci";
      Group = "flakey-ci";
      ExecStart = "${pkgs.python3}/bin/python3 ${./ci.py}";
      WorkingDirectory = "~";
    };
    wantedBy = [ "multi-user.target" ];
  };

  systemd.tmpfiles.rules = [
    "L+ /flag - - - - /sys/firmware/qemu_fw_cfg/by_name/flag/raw"
    # wipe old git cache entries every 15min
    "D /var/lib/flakey-ci/.cache/nix/gitv3 - - - 15m -"
  ];

  # disk usage management
  nix.gc = {
    automatic = true;
    # every 30 mins
    dates = "*:0/30";
    randomizedDelaySec = "2min";
  };

  systemd.services.fixup-mount = {
    serviceConfig = {
      ExecStart = "${pkgs.coreutils}/bin/chown -R flakey-ci:flakey-ci /var/lib/flakey-ci";
      Type = "oneshot";
    };
    after = [ "var-lib-flakey\\x2dci.mount" ];
    wantedBy = [ "var-lib-flakey\\x2dci.mount" ];
  };
}

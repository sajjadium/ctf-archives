{
  description = "CTF Challenge";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      lib = nixpkgs.lib;
      forAllSystems = f: lib.genAttrs lib.systems.flakeExposed (system: f (
        import nixpkgs {
          inherit system;
          overlays = [
            (final: prev: rec {
              jdk = prev.jdk17;
              maven = prev.maven.override { inherit jdk; };
              kotlin = prev.kotlin.override { jre = jdk; };
            })
          ];
        }
      ));
    in
    {
      packages = forAllSystems (pkgs: {
        default = with pkgs; maven.buildMavenPackage rec {
          pname = "challenge-server";
          version = "1.0";
          src = ./app;

          mvnHash = "sha256-8/awSTl4pHLzRwPQUD+QFLEmmLUFvBm8Yn8iq8CBtp4=";

          nativeBuildInputs = [ makeWrapper ];

          installPhase = ''
            install -Dm444 target/app-1.0.jar -t $out/lib
            makeWrapper "${jdk}/bin/java" "$out/bin/challenge-server" \
              --add-flags "-jar $out/lib/app-1.0.jar " \
              --prefix PATH : ${lib.makeBinPath [
                chromedriver
                chromium
              ]} \
              --set FONTCONFIG_FILE ${pkgs.fontconfig.out}/etc/fonts/fonts.conf \
              --set CHROME_BINARY ${pkgs.chromium}/bin/chromium
          '';
        };
        readFlag = with pkgs; stdenv.mkDerivation {
          name = "readflag";

          src = ./.;
          buildPhase = ''
            $CC ./readflag.c -o readflag
          '';
          installPhase = ''
            mkdir -p $out/bin
            cp readflag $out/bin
          '';
        };
      });
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          buildInputs = [ pkgs.bashInteractive ];
          packages = with pkgs; [ kotlin maven chromium chromedriver ];
          CHROME_BINARY = "${pkgs.chromium}/bin/chromium";
          shellHook = ''
            export SHELL=$(which bash)
          '';
        };
      });
    };
}

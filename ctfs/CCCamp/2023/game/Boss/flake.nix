{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixgl_.url = "github:guibou/nixGL";
  };

  outputs = { self, nixpkgs, poetry2nix, nixgl_ }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: (import nixpkgs {
        inherit system;
        overlays = [
          poetry2nix.overlay
          nixgl_.overlay
        ];
      }));

      overrides = pkgs: pkgs.poetry2nix.overrides.withDefaults (pyself: pysuper: {
        pyglet = pysuper.pyglet.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          propagatedBuildInputs = [

          ];
        });
        collision = pysuper.collision.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
        });
        viztracer = pysuper.viztracer.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools ];
        });
        objprint = pysuper.objprint.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools ];
        });
        numpy = pysuper.numpy.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools ];
        });
        pytiled-parser = pysuper.pytiled-parser.overridePythonAttrs (oldAttrs: {
          format = "pyproject"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools ];
        });
        dataclasses-jsonschema = pysuper.dataclasses-jsonschema.overridePythonAttrs (oldAttrs: {
          format = "pyproject"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools pysuper.setuptools-scm ];
        });
        cython = pysuper.cython.overridePythonAttrs (oldAttrs: {
          # format = "setuptools"; # for some reason poetry2nix patches this
          nativeBuildInputs = (oldAttrs.nativeBuildInputs or [ ]) ++ [ pysuper.setuptools pysuper.setuptools-scm ];
          version = "0.29.32";
        });
        mazelib = pysuper.mazelib.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          nativeBuildInputs = (oldAttrs.nativeBuildInputs or [ ]) ++ [ pysuper.setuptools-scm ];
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools pysuper.setuptools-scm ];
          propagatedBuildInputs = [
            pyself.numpy
            pyself.cython
          ];
          src = pkgs.fetchFromGitHub {
            owner = "john-science";
            repo = "mazelib";
            rev = "242c27c58241636c5c4ceb2d2ab46dd7ed86c293";
            hash = "sha256-srgWL7Zox22QbK2CWDIz+lPaDQycz+kiM/vhPR485j8=";
          };
          postPatch = ''
            substituteInPlace setup.py \
              --replace "cython>=0.27.0,<=0.29.32" "cython"
          '';
        });
        betterproto = pysuper.betterproto.overridePythonAttrs (oldAttrs: {
          src = pkgs.fetchFromGitHub {
            owner = "kilimnik";
            repo = "python-betterproto";
            rev = "pickle";
            hash = "sha256-I3a/APOlu4KnxRJjKsJjtMiTc++b/9F97Pu/zT9D8r0=";
          };
          nativeBuildInputs = (oldAttrs.nativeBuildInputs or [ ]) ++ [ pyself.setuptools-scm ];
        });
        aiochclient = pysuper.aiochclient.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          buildInputs = oldAttrs.buildInputs ++ [ pysuper.setuptools ];
        });
        pillow = pysuper.pillow.overridePythonAttrs (oldAttrs: {
          format = "setuptools"; # for some reason poetry2nix patches this
          src = pkgs.fetchFromGitHub {
            owner = "python-pillow";
            repo = "Pillow";
            rev = "9.5.0";
            hash = "sha256-EaDWjpCf3vGm7xRlaUaTn4L0f+OM/yDosE2RNaqZfj4=";
          };
          patches = [
            (pkgs.fetchpatch {
              name = "revert-multiple-paths-in-pkgconfig1.patch";
              url = "https://github.com/python-pillow/pillow/commit/17a0a2ee3eeb9df6e9fcf894d204911c7e6e4eef.patch";
              sha256 = "sha256-wAJfCYhBmXaVcVMwNBTk7kCpuJucAmetJTWtL155Ybc=";
              revert = true;
            })
            (pkgs.fetchpatch {
              name = "revert-multiple-paths-in-pkgconfig2.patch";
              url = "https://github.com/python-pillow/pillow/commit/a0492f796876c2a9b8ba445d72c771b84eff93a5.patch";
              sha256 = "sha256-vCBRczrl9v5QWrYkt85Nb06+ZXKt9GxTxg3djn4/m2o=";
              revert = true;
            })
            (pkgs.fetchpatch {
              name = "revert-multiple-paths-in-pkgconfig3.patch";
              url = "https://github.com/python-pillow/pillow/commit/04cf5e2cfc5dc1676efd9f5c8d605ddfccb0f9ee.patch";
              sha256 = "sha256-7uvNEUk6fBCBkwcqg6njhsAJGla11diz8KY966zsxew";
              revert = true;
            })
          ];
        });
      });
    in
    {
      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = self.packages.${system}.default;
        };
      });
      packages = forAllSystems (system: {
        default = pkgs.${system}.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          overrides = overrides pkgs.${system};
        };
        env = (pkgs.${system}.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          overrides = overrides pkgs.${system};
          editablePackageSources = {
            server = null;
            client = null;
            shared = null;
          };
        });
      });
      devShells = forAllSystems (system: {
        default = pkgs.${system}.mkShell {
          buildInputs = with pkgs.${system}; [
            poetry
            (pkgs.${system}.poetry2nix.mkPoetryEnv {
              projectDir = ./.;
              overrides = overrides pkgs.${system};
              editablePackageSources = {
                server = null;
                client = null;
                shared = null;
              };
            })
            buf
            tiled
            nixgl.nixGLIntel
            tracy
            clickhouse
          ];

          # add libararies to path, pyglet has some weird nix patches, but turns out they aren't necessary ?xD
          shellHook = ''
            export LD_LIBRARY_PATH="${pkgs.${system}.lib.makeLibraryPath (with pkgs.${system}; [
              libGL
              libGLU
              xorg.libX11
              gtk2-x11
              xorg.libXext
              fontconfig.lib
              freetype
              ffmpeg-full
              openal
              libpulseaudio
              xorg.libXi
              xorg.libXinerama
              xorg.libXxf86vm
              gdk-pixbuf
            ])}:$LD_LIBRARY_PATH"
            export PYTHONPATH="$(pwd)/src/client:$(pwd)/src/server:$(pwd)/src/shared:$PYTHONPATH"
          '';
        };
      });
    };
}

{
  description = "A very basic flake";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { flake-parts, ... } @ inputs: flake-parts.lib.mkFlake { inherit inputs; } {
    perSystem = { config, self', inputs', pkgs, system, ... }: {
      devShells.default = pkgs.mkShell {
        # venvShellHook needs venvDir set on the shell
        venvDir = ".venv";

        packages = with pkgs; [
          nodejs_latest
          playwright-driver.browsers
          uv
        ];

        # runs every time you enter the shell, after activation
        shellHook = ''
          export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
          export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true;
          uv sync --all-extras
          source .venv/bin/activate
          npm install
        '';
      };
    };
    # Declared systems that your flake supports. These will be enumerated in perSystem
    systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
  };
}

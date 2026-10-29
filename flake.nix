{
  description = "sunpy-sphinx-theme dev shell (provides Playwright browsers for NixOS)";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "https://channels.nixos.org/nixos-unstable/nixexprs.tar.zst";
  };

  outputs = { flake-parts, ... } @ inputs: flake-parts.lib.mkFlake { inherit inputs; } {
    perSystem = { config, self', inputs', pkgs, system, ... }: {
      devShells.default = pkgs.mkShell {
        # playwright-driver.browsers provides Firefox/Chromium patched to run on
        # NixOS. The pip `playwright` package reads PLAYWRIGHT_BROWSERS_PATH and
        # uses these browsers directly; its version must match whatever nixpkgs
        # pins here. nodejs is for the a11y env's npm install (axe-core).
        # bash is needed so `nix develop --command` can evaluate shellHook
        # (the devShell otherwise has no shell on PATH).
        packages = with pkgs; [
          bash
          nodejs_latest
          playwright-test
          playwright-driver.browsers
        ];

        shellHook = ''
          export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
          export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
          # Browsers installed by nix so no-op the install command in tox
          export PLAYWRIGHT_INSTALL_CMD="python -c pass"
        '';
      };
    };
    systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
  };
}

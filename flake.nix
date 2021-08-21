{
  description = "Discord overlay for NixOS, updated hourly";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        config.allowUnfree = true;
        overlays = [ self.overlay ];
        system = "x86_64-linux";
      };

      mkApp = drv: exePath: {
        type = "app";
        program = "${drv}${exePath}";
      };
    in {
      packages.x86_64-linux = {
        inherit (pkgs) discord discord-ptb discord-canary;
      };

      apps.x86_64-linux = {
        discord = mkApp pkgs.discord "/bin/discord";
        discord-ptb = mkApp pkgs.discord-ptb "/bin/discordptb";
        discord-canary = mkApp pkgs.discord-canary "/bin/discordcanary";
      };

      overlay = import ./default.nix;
    };
}

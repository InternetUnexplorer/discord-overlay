# Discord Overlay

![discord version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord&query=%24%5B%22discord%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)
![discord-ptb version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord-ptb&query=%24%5B%22discord-ptb%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)
![discord-canary version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord-canary&query=%24%5B%22discord-canary%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)

> **Warning**
> Now that [PR 197248](https://github.com/NixOS/nixpkgs/pull/197248) has landed,
> **this overlay is deprecated and might be discontinued in the future**. The
> only advantage this overlay has now over using the version in Nixpkgs is that
> you'll get the latest version a day or two earlier.

This is a Nixpkgs overlay that provides the latest[^1] versions of the Discord
desktop apps. You can use it with or without flakes:

<details>
<summary>With flakes (preferred)</summary>

To run it once:

```bash
$ nix run github:InternetUnexplorer/discord-overlay#discord-canary --update-input nixpkgs --no-write-lock-file
```

To add it to your NixOS configuration:

```nix
# /etc/nixos/flake.nix
# Your configuration will probably look different; this is just an example!
{
  description = "Example NixOS configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    discord-overlay.url = "github:InternetUnexplorer/discord-overlay";
    discord-overlay.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, discord-overlay }: {
    nixosConfigurations.example = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ({ ... }: { nixpkgs.overlays = [ discord-overlay.overlays.default ]; })
        ./configuration.nix
      ];
    };
  };
}
```

</details>

<details>
<summary>Without flakes (not recommended)</summary>

To use it with `nix-env`:

```nix
# ~/.config/nixpkgs/overlays.nix
[
  (import (builtins.fetchTarball {
    url = "https://github.com/InternetUnexplorer/discord-overlay/archive/main.tar.gz";
  }))
  # ...
]
```

To add it to your NixOS configuration:

```nix
# /etc/nixos/configuration.nix
{ config, pkgs, lib, ... }:

{
  nixpkgs.overlays = [
    (import (builtins.fetchTarball {
      url = "https://github.com/InternetUnexplorer/discord-overlay/archive/main.tar.gz";
    }))
  ];
  # ...
}
```

</details>

You can find an explanation of how the update process works
[here](./EXPLANATION.md). The old README is available
[here](https://github.com/InternetUnexplorer/discord-overlay/blob/647652fcbeb05f8ce12953d03495d60a84d1e101/README.md).
Licensed under the [Unlicense](https://unlicense.org).

[^1]: Checking for updates happens every 30 minutes.

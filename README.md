# Discord Overlay

![discord version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord&query=%24%5B%22discord%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)
![discord-ptb version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord-ptb&query=%24%5B%22discord-ptb%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)
![discord-canary version](https://img.shields.io/badge/dynamic/json?style=flat-square&color=%235865F2&label=discord-canary&query=%24%5B%22discord-canary%22%5D.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FInternetUnexplorer%2Fdiscord-overlay%2Fmain%2Fversions.json)

## What is this?

This is a [Nixpkgs][1] overlay that attempts to automatically keep the [Discord
desktop app][2] packages up-to-date.

Specifically, it updates the `discord`, `discord-ptb`, and `discord-canary`
packages.

## How do I use it?

You can use it as an overlay, for example in `~/.config/nixpkgs/overlays.nix`:

```nix
[
  (import (builtins.fetchTarball {
    url = "https://github.com/InternetUnexplorer/discord-overlay/archive/main.tar.gz";
  }))
]
```

If you have a version of Nix that supports [flakes][3], you can also use it as a
flake! For example:

```sh
$ nix run github:InternetUnexplorer/discord-overlay#discord-canary --update-input nixpkgs --no-write-lock-file
```

## Why did you make this?

Every once in a while, Discord gets an update and won't let you use it until you
update it:

![Discord update dialog](https://i.postimg.cc/VLK8XvDZ/discord-update.png)

Unfortunately, some times it takes a few days for the update to make its way to
the unstable channel, so in the meantime I've had to do things like:

- Use the web version (_gasp_)
- Install it from Flatpak (why does my mouse cursor look weird?)
- Update it myself (but that's _so_ difficult)
- Cry (I usually do this anyway)

This is a (probably overkill) solution to that problem that may or may not work
(but I think it should).

## How does it work?

I have a little [GCE instance][6] that checks for new versions every 30 minutes
(using `update.py check`). When there's an update, the script sends a
[`repository_dispatch`][7] event to this repository.

That event triggers the [update workflow][4], which updates `versions.json`
(using `update.py update`) and makes sure the package still builds before
pushing the changes.

[EXPLANATION.md](./EXPLANATION.md) contains more information about how the
update process works.

## What am I allowed to do with it?

This is licensed under the [Unlicense][5]. Feel free to use any part of this
repository in your own projects without having to provide credit.

[1]: https://github.com/NixOS/nixpkgs
[2]: https://discord.com/download
[3]: https://nixos.wiki/wiki/Flakes
[4]: https://github.com/InternetUnexplorer/discord-overlay/blob/main/.github/workflows/update.yml
[5]: https://unlicense.org
[6]: https://cloud.google.com/free
[7]: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#repository_dispatch
[8]: https://gist.github.com/InternetUnexplorer/9ec81077e4e000788038b611e7e23990

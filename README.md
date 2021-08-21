# Discord Overlay

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
$ nix run github:InternetUnexplorer/discord-overlay#discord-canary --recreate-lock-file
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

There is an [action][4] that checks for new versions every hour and updates
`versions.json` accordingly. This means it won't work if an update requires
manual intervention (e.g. adding a dependency), but there's really no getting
around that as far as I know.

## What am I allowed to do with it?

This is licensed under the [Unlicense][5]. Feel free to use any part of this
repository in your own projects without having to provide credit.

[1]: https://github.com/NixOS/nixpkgs
[2]: https://discord.com/download
[3]: https://nixos.wiki/wiki/Flakes
[4]: https://github.com/InternetUnexplorer/discord-overlay/blob/main/.github/workflows/update.yml
[5]: https://unlicense.org

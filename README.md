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
$ nix run github:InternetUnexplorer/discord-overlay#discord-canary
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

Both parts use the same script (`update.py`), and `versions.json` is different
on the server's side (it contains a map of `pname` to `version`, instead of to
an object containing the `version`, `url`, and `sha256`), which can be a bit
confusing.

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

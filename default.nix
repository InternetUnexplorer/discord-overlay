final: prev:

let versions = builtins.fromJSON (builtins.readFile ./versions.json);

in {
  discord = prev.discord.overrideAttrs (_: {
    inherit (versions.discord) version;
    src = builtins.fetchurl { inherit (versions.discord) url sha256; };
  });

  discord-ptb = prev.discord-ptb.overrideAttrs (_: {
    inherit (versions.discord-ptb) version;
    src = builtins.fetchurl { inherit (versions.discord-ptb) url sha256; };
  });

  discord-canary = prev.discord-canary.overrideAttrs (_: {
    inherit (versions.discord-canary) version;
    src = builtins.fetchurl { inherit (versions.discord-canary) url sha256; };
  });
}

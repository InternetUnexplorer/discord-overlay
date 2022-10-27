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

    # https://github.com/InternetUnexplorer/discord-overlay/issues/10
    postInstall = (prev.postInstall or "") + ''
      cp -n ${prev.electron_17}/lib/electron/chrome_crashpad_handler $out/opt/DiscordCanary
    '';
  });
}

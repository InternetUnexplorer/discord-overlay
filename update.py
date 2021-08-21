#!/usr/bin/env python3

import json
from re import search
from subprocess import run
from sys import argv
from typing import Dict
from urllib.request import Request, urlopen


################################################


def get_redirect_location(url: str, user_agent: str = "curl/7.76.1") -> str:
    """Follow redirects on `url` and return the final URL."""
    return urlopen(Request(url, headers={"User-Agent": user_agent})).geturl()


def get_url(pname: str) -> str:
    """Get the URL for package `pname`."""
    url_mid = {"discord": "", "discord-ptb": "/ptb", "discord-canary": "/canary"}[pname]
    url = f"https://discord.com/api/download{url_mid}?platform=linux&format=tar.gz"
    return get_redirect_location(url)


def get_version(pname: str, url: str) -> str:
    """Extract the package version from the url returned by `get_url`."""
    match = search(r"/(\d+\.\d+\.\d+)/(\w+(?:-\w+)?)-(\d+\.\d+\.\d+)\.tar\.gz$", url)
    # Assert that the package name matches.
    assert match[2] == pname
    # As a sanity check, also assert that the versions match.
    assert match[1] == match[3]
    # Return the version.
    return match[1]


def get_sha256(url: str) -> str:
    """Get the sha256 of `url` using `nix-prefetch-url`."""
    process = run(
        ["nix-prefetch-url", "--type", "sha256", url], capture_output=True, check=True
    )
    return process.stdout.strip().decode("utf-8")


################################################

VersionDict = Dict[str, Dict[str, str]]


def load_versions() -> VersionDict:
    """Load the version information from `versions.json`"""
    with open("versions.json", "r") as file:
        return json.load(file)


def save_versions(versions: VersionDict) -> None:
    """Save the version information to `versions.json`"""
    with open("versions.json", "w") as file:
        json.dump(versions, file, sort_keys=True, indent=2)
        file.write("\n")


################################################


def check_for_updates() -> None:
    """Get the list of packages that have a newer version available."""
    print("checking for updates...")

    # Make a dict mapping each package to a tuple containing both its current and latest
    # version.
    versions_json = load_versions()
    versions = {
        pname: (versions_json[pname]["version"], get_version(pname, get_url(pname)))
        for pname in ["discord", "discord-ptb", "discord-canary"]
    }

    for pname, (current, latest) in versions.items():
        print(
            f"  {pname}: {current}",
            "(up-to-date)" if current == latest else f"-> {latest}",
        )

    # Set the `packages` output to the list of packages that need to be updated.
    packages_to_update = [
        pname for pname, details in versions.items() if details[0] != details[1]
    ]
    print("::set-output", f"name=packages::{json.dumps(packages_to_update)}")


def update_package(pname: str) -> None:
    """Update the values for package `pname` in `versions.json`."""
    print(f"updating {pname}...")

    # Get the new URL, version, and sha256.
    url = get_url(pname)
    version = get_version(pname, url)
    sha256 = get_sha256(url)

    versions = load_versions()
    old_version = versions[pname]["version"]
    print(f"  version: {old_version} -> {version}")
    print(f"      url: {url}")
    print(f"   sha256: {sha256}")
    print()

    # Update `versions.json` with the new values.
    versions[pname]["version"] = version
    versions[pname]["url"] = url
    versions[pname]["sha256"] = sha256
    save_versions(versions)

    # Commit the new `versions.json`.
    run(
        [
            "git",
            "commit",
            "versions.json",
            "-m",
            f"{pname}: {old_version} -> {version}",
        ],
        check=True,
    )


################################################


if __name__ == "__main__":
    if argv[1] == "matrix":
        check_for_updates()
    elif argv[1] == "update":
        update_package(argv[2])
    else:
        raise ValueError()

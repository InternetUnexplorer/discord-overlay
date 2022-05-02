#!/usr/bin/env python3

# This script is used in two places:
# - On a server running `update.py check` periodically
# - In the GitHub Actions update workflow (`update.py update`)
#
# Check EXPLANATION.md for more information on how the update process works.
#
# In order to send `repository_dispatch` events, $GITHUB_TOKEN needs to be set.
# The token needs to have the `repo` scope.

import json
from argparse import ArgumentParser
from os import environ, path
from re import search
from subprocess import run
from typing import Dict, Union
from urllib.request import Request, urlopen

################################################

GITHUB_REPOSITORY = "InternetUnexplorer/discord-overlay"

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

VersionDict = Dict[str, Union[str, Dict[str, str]]]


def load_versions() -> VersionDict:
    """Load the version information from `versions.json`"""
    with open("versions.json", "r") as file:
        return json.load(file)


def save_versions(versions: VersionDict) -> None:
    """Save the version information to `versions.json`"""
    with open("versions.json", "w") as file:
        json.dump(versions, file, sort_keys=True, indent=2)
        file.write("\n")


def init_versions() -> None:
    """Initialize the check-side `versions.json` based on the one in the repository"""
    url = f"https://github.com/{GITHUB_REPOSITORY}/raw/main/versions.json"
    versions = json.loads(urlopen(url).read().decode("utf-8"))
    save_versions({pname: data["version"] for pname, data in versions.items()})


################################################


def trigger_update(pname: str, version_old: str, version_new: str) -> None:
    """Send a `repository_dispatch` event to trigger the `update` workflow."""

    data = {
        # We only ever send a repository dispatch to update a package, so here we misuse the
        # `event_type` field to show a helpful description of what's being updated.
        "event_type": f"{pname}: {version_old} -> {version_new}",
        "client_payload": {"package": pname},
    }

    request = Request(f"https://api.github.com/repos/{GITHUB_REPOSITORY}/dispatches")
    request.add_header("Accept", "application/vnd.github.v3+json")
    request.add_header("Authorization", f"token {environ['GITHUB_TOKEN']}")

    urlopen(request, data=json.dumps(data).encode("utf-8"))


def check_for_updates() -> None:
    """Check for updates, and call `trigger_update` to update out-of-date packages."""

    if not path.isfile("versions.json"):
        print("warning: versions.json does not exist, creating it")
        init_versions()

    versions = load_versions()

    print("checking for updates...")
    for pname in ["discord", "discord-ptb", "discord-canary"]:
        old_version = versions[pname]
        new_version = get_version(pname, get_url(pname))

        if old_version != new_version:
            print(f"  {pname}: updating from {old_version} to {new_version}...")
            # Send a `repository_dispatch` event to update the package.
            trigger_update(pname, old_version, new_version)
            # Update `versions.json` with the new version.
            # This is done regardless of whether the update succeeded, to prevent successive
            # `repository_dispatch` events being sent when an update fails.
            versions[pname] = new_version
            save_versions(versions)
        else:
            print(f"  {pname}: up-to-date ({old_version})")


################################################


def update_package(pname: str) -> None:
    """Update the values for package `pname` in `versions.json`."""
    print(f"updating {pname}...")

    # Get the new URL, version, and sha256.
    url = get_url(pname)
    version = get_version(pname, url)
    sha256 = get_sha256(url)

    # Load the version information from `versions.json`.
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
    parser = ArgumentParser()
    commands = parser.add_subparsers(required=True, dest="command")
    commands.add_parser("check")
    commands.add_parser("update").add_argument("pname", type=str)

    args = parser.parse_args()
    if args.command == "check":
        check_for_updates()
    elif args.command == "update":
        update_package(args.pname)

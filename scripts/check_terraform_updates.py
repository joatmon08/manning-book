#!/usr/bin/env python3
"""Report Terraform CLI and provider versions that need a bump.

Scans chapter lockfiles under ch*/ and the Terraform version pinned in
README.md / GitHub Actions. Compares against the HashiCorp registry and
releases API. Exits 0 when everything is current, 1 when at least one
newer stable version is available, 2 on unexpected errors.

Intended for a monthly Cursor Automation that opens a PR when updates
exist (Terraform rarely ships majors; minor/patch bumps still matter).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

from packaging.version import InvalidVersion, Version

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "https://registry.terraform.io/v1/providers"
TF_RELEASES = "https://releases.hashicorp.com/terraform/index.json"
USER_AGENT = "manning-book-terraform-update-check/1.0"

LOCK_PROVIDER_RE = re.compile(
    r'provider\s+"(?P<source>[^"]+)"\s*\{\s*version\s*=\s*"(?P<version>[^"]+)"',
    re.MULTILINE,
)
TF_PIN_RE = re.compile(
    r"(?:terraform_version:\s*|Install Terraform\s+)(?P<version>\d+\.\d+\.\d+)"
)
STABLE_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def parse_stable(version: str) -> Version | None:
    if not STABLE_VERSION_RE.match(version):
        return None
    try:
        return Version(version)
    except InvalidVersion:
        return None


def bump_kind(current: Version, latest: Version) -> str | None:
    if latest <= current:
        return None
    if latest.major > current.major:
        return "major"
    if latest.minor > current.minor:
        return "minor"
    return "patch"


def inventory_lockfiles(root: Path) -> dict[str, Version]:
    """Return the highest locked version per provider source under ch*/."""
    locked: dict[str, Version] = {}
    for lockfile in sorted(root.glob("ch*/**/.terraform.lock.hcl")):
        text = lockfile.read_text(encoding="utf-8")
        for match in LOCK_PROVIDER_RE.finditer(text):
            source = match.group("source")
            version = parse_stable(match.group("version"))
            if version is None:
                continue
            if source not in locked or version > locked[source]:
                locked[source] = version
    return locked


def inventory_terraform_cli(root: Path) -> Version | None:
    candidates: list[Version] = []
    for path in [
        root / "README.md",
        *sorted((root / ".github" / "workflows").glob("*.yml")),
    ]:
        if not path.exists():
            continue
        for match in TF_PIN_RE.finditer(path.read_text(encoding="utf-8")):
            version = parse_stable(match.group("version"))
            if version is not None:
                candidates.append(version)
    return max(candidates) if candidates else None


def latest_provider_version(namespace: str, name: str) -> Version:
    data = fetch_json(f"{REGISTRY}/{namespace}/{name}/versions")
    versions: list[Version] = []
    for entry in data.get("versions", []):
        version = parse_stable(entry.get("version", ""))
        if version is not None:
            versions.append(version)
    if not versions:
        raise RuntimeError(f"no stable versions for {namespace}/{name}")
    return max(versions)


def latest_terraform_version() -> Version:
    data = fetch_json(TF_RELEASES)
    versions: list[Version] = []
    for raw in data.get("versions", {}):
        version = parse_stable(raw)
        if version is not None:
            versions.append(version)
    if not versions:
        raise RuntimeError("no stable Terraform releases found")
    return max(versions)


def split_registry_source(source: str) -> tuple[str, str]:
    # registry.terraform.io/hashicorp/google -> hashicorp, google
    parts = source.split("/")
    if len(parts) < 2:
        raise ValueError(f"unrecognized provider source: {source}")
    return parts[-2], parts[-1]


def format_row(name: str, current: Version | str, latest: Version | str, action: str) -> str:
    return f"{name:40} {str(current):12} {str(latest):12} {action}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a table",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        locked = inventory_lockfiles(root)
        terraform_current = inventory_terraform_cli(root)
        bumps: list[dict] = []
        rows: list[str] = []

        if terraform_current is None:
            rows.append(format_row("terraform (cli)", "missing", "?", "ERROR"))
        else:
            tf_latest = latest_terraform_version()
            kind = bump_kind(terraform_current, tf_latest)
            action = f"{kind.upper()} -> {tf_latest}" if kind else "current"
            rows.append(format_row("terraform (cli)", terraform_current, tf_latest, action))
            if kind is not None:
                bumps.append(
                    {
                        "kind": "terraform",
                        "name": "terraform",
                        "current": str(terraform_current),
                        "latest": str(tf_latest),
                        "bump": kind,
                    }
                )

        for source in sorted(locked):
            current = locked[source]
            namespace, name = split_registry_source(source)
            latest = latest_provider_version(namespace, name)
            kind = bump_kind(current, latest)
            label = f"{namespace}/{name}"
            action = f"{kind.upper()} -> {latest}" if kind else "current"
            rows.append(format_row(label, current, latest, action))
            if kind is not None:
                bumps.append(
                    {
                        "kind": "provider",
                        "name": label,
                        "source": source,
                        "current": str(current),
                        "latest": str(latest),
                        "bump": kind,
                    }
                )

        versions_seen: dict[str, set[str]] = defaultdict(set)
        for lockfile in root.glob("ch*/**/.terraform.lock.hcl"):
            text = lockfile.read_text(encoding="utf-8")
            for match in LOCK_PROVIDER_RE.finditer(text):
                version = parse_stable(match.group("version"))
                if version is not None:
                    versions_seen[match.group("source")].add(str(version))
        drift = {
            source: sorted(versions, key=Version)
            for source, versions in versions_seen.items()
            if len(versions) > 1
        }

        payload = {
            "bumps": bumps,
            "drift": drift,
            "has_update": bool(bumps),
        }

        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(format_row("COMPONENT", "CURRENT", "LATEST", "STATUS"))
            print("-" * 80)
            for row in rows:
                print(row)
            if drift:
                print("\nMixed versions across chapter lockfiles:")
                for source, versions in sorted(drift.items()):
                    print(f"  {source}: {versions}")
            if bumps:
                print("\nUpgrades available:")
                for bump in bumps:
                    print(
                        f"  - {bump['name']}: {bump['current']} -> {bump['latest']}"
                        f" ({bump['bump']})"
                    )
            else:
                print("\nNo Terraform or provider upgrades available.")

        return 1 if bumps else 0
    except (urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

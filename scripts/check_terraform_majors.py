#!/usr/bin/env python3
"""Report Terraform CLI and provider major versions that need a bump.

Scans chapter lockfiles under ch*/ and the Terraform version pinned in
README.md / GitHub Actions. Compares against the HashiCorp registry and
releases API. Exits 0 when no major upgrades are available, 1 when at
least one major bump is available, 2 on unexpected errors.

Intended for Cursor Automations (and optional CI) that open a PR only
when a new major line exists.
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
USER_AGENT = "manning-book-terraform-major-check/1.0"

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


def latest_provider_versions(namespace: str, name: str) -> tuple[Version, dict[int, Version]]:
    data = fetch_json(f"{REGISTRY}/{namespace}/{name}/versions")
    by_major: dict[int, Version] = {}
    for entry in data.get("versions", []):
        version = parse_stable(entry.get("version", ""))
        if version is None:
            continue
        current = by_major.get(version.major)
        if current is None or version > current:
            by_major[version.major] = version
    if not by_major:
        raise RuntimeError(f"no stable versions for {namespace}/{name}")
    latest = max(by_major.values())
    return latest, by_major


def latest_terraform_versions() -> tuple[Version, dict[int, Version]]:
    data = fetch_json(TF_RELEASES)
    by_major: dict[int, Version] = {}
    for raw in data.get("versions", {}):
        version = parse_stable(raw)
        if version is None:
            continue
        current = by_major.get(version.major)
        if current is None or version > current:
            by_major[version.major] = version
    if not by_major:
        raise RuntimeError("no stable Terraform releases found")
    latest = max(by_major.values())
    return latest, by_major


def split_registry_source(source: str) -> tuple[str, str]:
    # registry.terraform.io/hashicorp/google -> hashicorp, google
    parts = source.split("/")
    if len(parts) < 2:
        raise ValueError(f"unrecognized provider source: {source}")
    return parts[-2], parts[-1]


def major_gap(current: Version, by_major: dict[int, Version]) -> Version | None:
    newer_majors = [major for major in by_major if major > current.major]
    if not newer_majors:
        return None
    target_major = max(newer_majors)
    return by_major[target_major]


def format_row(name: str, current: Version | str, latest: Version, action: str) -> str:
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
            tf_latest, tf_by_major = latest_terraform_versions()
            target = major_gap(terraform_current, tf_by_major)
            action = (
                f"MAJOR -> {target}"
                if target is not None
                else ("current major" if terraform_current.major == tf_latest.major else "ok")
            )
            rows.append(format_row("terraform (cli)", terraform_current, tf_latest, action))
            if target is not None:
                bumps.append(
                    {
                        "kind": "terraform",
                        "name": "terraform",
                        "current": str(terraform_current),
                        "latest": str(tf_latest),
                        "target_major": str(target),
                    }
                )

        # Group identical sources; keep deterministic order.
        for source in sorted(locked):
            current = locked[source]
            namespace, name = split_registry_source(source)
            latest, by_major = latest_provider_versions(namespace, name)
            target = major_gap(current, by_major)
            label = f"{namespace}/{name}"
            action = (
                f"MAJOR -> {target}"
                if target is not None
                else ("current major" if current.major == latest.major else "ok")
            )
            rows.append(format_row(label, current, latest, action))
            if target is not None:
                bumps.append(
                    {
                        "kind": "provider",
                        "name": label,
                        "source": source,
                        "current": str(current),
                        "latest": str(latest),
                        "target_major": str(target),
                    }
                )

        # Surface providers that appear only in some lockfiles with mixed majors.
        majors_seen: dict[str, set[int]] = defaultdict(set)
        for lockfile in root.glob("ch*/**/.terraform.lock.hcl"):
            text = lockfile.read_text(encoding="utf-8")
            for match in LOCK_PROVIDER_RE.finditer(text):
                version = parse_stable(match.group("version"))
                if version is not None:
                    majors_seen[match.group("source")].add(version.major)
        drift = {
            source: sorted(majors)
            for source, majors in majors_seen.items()
            if len(majors) > 1
        }

        payload = {
            "bumps": bumps,
            "drift": drift,
            "has_major_bump": bool(bumps),
        }

        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(format_row("COMPONENT", "CURRENT", "LATEST", "STATUS"))
            print("-" * 80)
            for row in rows:
                print(row)
            if drift:
                print("\nMixed majors across chapter lockfiles:")
                for source, majors in sorted(drift.items()):
                    print(f"  {source}: {majors}")
            if bumps:
                print("\nMajor upgrades available:")
                for bump in bumps:
                    print(
                        f"  - {bump['name']}: {bump['current']} -> {bump['target_major']}"
                        f" (latest on that line / overall {bump['latest']})"
                    )
            else:
                print("\nNo Terraform or provider major upgrades available.")

        return 1 if bumps else 0
    except (urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

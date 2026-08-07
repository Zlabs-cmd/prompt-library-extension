#!/usr/bin/env python3
"""Securely install OPENAI_API_KEY across the Zlabs-cmd portfolio.

Requires:
  - Python 3.10+
  - GitHub CLI (`gh`) authenticated as an account with Actions secret write access

The secret is read with getpass and sent to `gh secret set` over stdin. It is never
written to disk, printed, or passed as a command-line argument.
"""

from __future__ import annotations

import getpass
import json
import shutil
import subprocess
import sys

REPOSITORIES = [
    "Zlabs-cmd/prompt-library-extension",
    "Zlabs-cmd/golden-moving-platform",
    "Zlabs-cmd/cruise-line-order-au",
    "Zlabs-cmd/ClosedLab-Landing",
    "Zlabs-cmd/Moving-Operations-Backend-Application",
    "Zlabs-cmd/real-estate-leads",
    "Zlabs-cmd/Insurance",
    "Zlabs-cmd/Mezuzah-Investments-and-Banking",
    "Zlabs-cmd/ascendants_marketing_app",
    "Zlabs-cmd/WareHouse",
    "Zlabs-cmd/Priority-Moving-App",
    "Zlabs-cmd/LowesVanlines-LandingPage",
    "Zlabs-cmd/MobDial-Platform",
    "Zlabs-cmd/ClosedLab-Workspace",
    "Zlabs-cmd/timeless-relationshi",
    "Zlabs-cmd/Priv-MobDial-Operations-Dashboard",
    "Zlabs-cmd/golden-moving-llc",
    "Zlabs-cmd/FreightLine",
    "Zlabs-cmd/pmg-ops-dashboard",
    "Zlabs-cmd/Budget-Movers",
    "Zlabs-cmd/Silv-Website",
    "Zlabs-cmd/lucas_dispatch",
    "Zlabs-cmd/SilveraOps-SaaS",
]

SECRET_NAME = "OPENAI_API_KEY"


def run(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    if shutil.which("gh") is None:
        print("ERROR: GitHub CLI (`gh`) is not installed or not on PATH.", file=sys.stderr)
        return 2

    auth = run(["gh", "auth", "status"])
    if auth.returncode != 0:
        print("ERROR: GitHub CLI is not authenticated.", file=sys.stderr)
        if auth.stderr:
            print(auth.stderr.strip(), file=sys.stderr)
        return 2

    print(
        "Use ONLY a newly created/rotated OpenAI API key. "
        "Do not reuse a key that has appeared in chat, logs, source code, or shell history."
    )
    key = getpass.getpass("Fresh OPENAI_API_KEY: ").strip()
    if not key:
        print("ERROR: Empty key; nothing changed.", file=sys.stderr)
        return 2

    failures: list[tuple[str, str]] = []
    installed: list[str] = []

    try:
        for repo in REPOSITORIES:
            result = run(
                ["gh", "secret", "set", SECRET_NAME, "--repo", repo],
                input_text=key,
            )
            if result.returncode == 0:
                installed.append(repo)
                print(f"SET      {repo}")
            else:
                reason = (result.stderr or result.stdout or "unknown gh error").strip()
                failures.append((repo, reason))
                print(f"FAILED   {repo}", file=sys.stderr)
    finally:
        key = ""  # Drop our reference as soon as the writes are complete.

    verification_failures: list[tuple[str, str]] = []
    for repo in installed:
        result = run(
            ["gh", "secret", "list", "--repo", repo, "--app", "actions", "--json", "name"]
        )
        if result.returncode != 0:
            verification_failures.append((repo, (result.stderr or "list failed").strip()))
            print(f"VERIFY?  {repo}", file=sys.stderr)
            continue

        try:
            names = {item["name"] for item in json.loads(result.stdout)}
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            verification_failures.append((repo, f"invalid gh JSON: {exc}"))
            print(f"VERIFY?  {repo}", file=sys.stderr)
            continue

        if SECRET_NAME in names:
            print(f"VERIFIED {repo}")
        else:
            verification_failures.append((repo, f"{SECRET_NAME} not listed"))
            print(f"MISSING  {repo}", file=sys.stderr)

    print()
    print(f"Repositories targeted: {len(REPOSITORIES)}")
    print(f"Secret writes succeeded: {len(installed)}")
    print(f"Secret write failures: {len(failures)}")
    print(f"Verification failures: {len(verification_failures)}")

    if failures:
        print("\nWrite failures:", file=sys.stderr)
        for repo, reason in failures:
            print(f"- {repo}: {reason}", file=sys.stderr)

    if verification_failures:
        print("\nVerification failures:", file=sys.stderr)
        for repo, reason in verification_failures:
            print(f"- {repo}: {reason}", file=sys.stderr)

    return 0 if not failures and not verification_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

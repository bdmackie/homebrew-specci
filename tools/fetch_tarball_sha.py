#!/usr/bin/env python3
import hashlib
import os
import pathlib
import sys
import textwrap
from urllib.error import HTTPError
from urllib.request import Request, urlopen

GITHUB_OWNER = "bdmackie"
GITHUB_REPO = "specci-client"


def download_tarball(version: str, dest: pathlib.Path) -> str:
    token = os.environ.get("SPECCI_CLIENT_GITHUB_TOKEN")
    headers = {"User-Agent": "specci-fetch-tarball"}
    if token:
        print(f"Using GitHub token: {token}")
        headers["Authorization"] = f"Bearer {token}"

    # Preliminary test: try to access README.md to confirm repo + token visibility
    readme_url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/main/README.md"
    readme_req = Request(readme_url, headers=headers)
    print(f"Reading README.md from {readme_url}...")
    try:
        with urlopen(readme_req) as _:
            print("... README.md access OK (authentication and repo visibility confirmed)")
    except HTTPError as e:
        print(f"Warning: Could not access README.md (HTTP {e.code}).", file=sys.stderr)
        if not token:
            print("         Token missing: set SPECCI_CLIENT_GITHUB_TOKEN for private repo access.", file=sys.stderr)
        else:
            print("         Token may lack permissions or repository access settings.", file=sys.stderr)
        # Continue anyway—the tarball fetch will report detailed errors

    """Download the GitHub tag tarball for a version like '0.1.0'."""
    tag = f"v{version}"

    # Old GitHub archive URL (kept for reference; fine‑grained PATs often cannot access this for private repos)
    # old_url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/tags/{tag}.tar.gz"

    # New recommended API tarball endpoint (supports fine‑grained PAT authentication)
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/tarball/{tag}"

    print(f"Downloading {url}...")

    req = Request(url, headers=headers)
    try:
        with urlopen(req) as resp, dest.open("wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
    except HTTPError as e:
        if e.code == 404:
            print(f"Error: Version {version} (tag {tag}) not found.", file=sys.stderr)
            print(f"       Check available tags at: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/tags", file=sys.stderr)
            if not token:
                print("       Hint: if this is a private repo, set SPECCI_CLIENT_GITHUB_TOKEN with a GitHub personal access token.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
            sys.exit(1)

    return url


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: fetch_tarball_sha.py <version>")
        print("Example: fetch_tarball_sha.py 0.1.0")
        sys.exit(1)

    version = sys.argv[1]
    dest = pathlib.Path(f"/tmp/specci-client-{version}.tar.gz")

    url = download_tarball(version, dest)
    sha = sha256_file(dest)

    print()
    print("Tarball downloaded:", dest)
    print("URL:   ", url)
    print("SHA256:", sha)
    print()
    print("Formula snippet:")
    print(textwrap.dedent(f"""
        url "{url}"
        sha256 "{sha}"
    """))
    print()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import pathlib
import re
import sys

from fetch_tarball_sha import download_tarball, sha256_file

FORMULA_PATH = pathlib.Path("Formula/specci.rb")


def update_formula(version: str) -> None:
    if not FORMULA_PATH.exists():
        raise SystemExit(f"Formula not found at {FORMULA_PATH}")

    tarball_path = pathlib.Path(f"/tmp/specci-client-{version}.tar.gz")
    url = download_tarball(version, tarball_path)
    sha = sha256_file(tarball_path)

    text = FORMULA_PATH.read_text()

    # Replace url line
    text = re.sub(
        r'url "[^"]+"',
        f'url "{url}"',
        text,
    )

    # Replace sha256 line
    text = re.sub(
        r'sha256 "[^"]+"',
        f'sha256 "{sha}"',
        text,
    )

    FORMULA_PATH.write_text(text)
    print(f"Updated {FORMULA_PATH} to version {version}")
    print(f"  url: {url}")
    print(f"  sha256: {sha}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: update_formula.py <version>")
        print("Example: update_formula.py 0.1.1")
        raise SystemExit(1)

    print()
    version = sys.argv[1]
    update_formula(version)
    print()

if __name__ == "__main__":
    main()

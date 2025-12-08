#!/usr/bin/env python3
import pathlib
import re
import sys
from pathlib import Path

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

from fetch_tarball_sha import download_tarball, sha256_file


def update_formula_ssh(version: str, formula_path: pathlib.Path | None = None) -> None:
    if formula_path is None:
        formula_path = pathlib.Path("Formula/specci.rb")
    
    if not formula_path.exists():
        raise SystemExit(f"Formula not found at {formula_path}")

    tarball_path = pathlib.Path(f"/tmp/specci-client-{version}.tar.gz")
    url = download_tarball(version, tarball_path)
    sha = sha256_file(tarball_path)

    text = formula_path.read_text()

    # Replace url line
    text = re.sub(
        r'url "[^"]+"',
        f'url "{url}"',
        text,
    )

    # Replace sha256 line
    text = re.sub(
        r'tag: "[^"]+"',
        f'tag: "v{version}"',
        text,
    )

    # Replace sha256 line
    text = re.sub(
        r'sha256 "[^"]+"',
        f'sha256 "{sha}"',
        text,
    )

    formula_path.write_text(text)
    print(f"Updated {formula_path} to version {version}")
    print(f"  url: {url}")
    print(f"  sha256: {sha}")


def update_formula_https(version: str, formula_path: pathlib.Path | None = None) -> None:
    if formula_path is None:
        formula_path = pathlib.Path("Formula/specci.rb")
    
    if not formula_path.exists():
        raise SystemExit(f"Formula not found at {formula_path}")

    tarball_path = pathlib.Path(f"/tmp/specci-client-{version}.tar.gz")
    url = download_tarball(version, tarball_path)
    sha = sha256_file(tarball_path)

    text = formula_path.read_text()

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

    formula_path.write_text(text)
    print(f"Updated {formula_path} to version {version}")
    print(f"  url: {url}")
    print(f"  sha256: {sha}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: update_formula.py <version>")
        print("Example: update_formula.py 0.1.1")
        raise SystemExit(1)

    print()
    version = sys.argv[1]
    update_formula_https(version)
    print()

if __name__ == "__main__":
    main()

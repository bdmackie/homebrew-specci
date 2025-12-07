#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FORMULA_PATH = REPO_ROOT / "Formula" / "specci.rb"


def run(cmd: list[str], *, check: bool = True, capture_output: bool = False, text: bool = True):
    """Small wrapper around subprocess.run for convenience."""
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=check,
        capture_output=capture_output,
        text=text,
    )


def ensure_formula_exists() -> None:
    if not FORMULA_PATH.exists():
        print(f"Error: Formula file not found at {FORMULA_PATH}", file=sys.stderr)
        print("Make sure you're running this inside the homebrew-specci repo.", file=sys.stderr)
        sys.exit(1)


def update_formula(version: str) -> None:
    """Call the existing update_formula.py helper."""
    print(f"== Updating formula for version {version} ==")
    try:
        run([sys.executable, "tools/update_formula.py", version])
    except subprocess.CalledProcessError as e:
        print("Error: update_formula.py failed.", file=sys.stderr)
        if e.stdout:
            print("--- stdout ---")
            print(e.stdout)
        if e.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)


def show_diff() -> None:
    """Show the git diff for the formula file."""
    print("\n== Git diff (Formula/specci.rb) ==")
    result = run(["git", "diff", "--", "Formula/specci.rb"], capture_output=True)
    diff = result.stdout.strip()
    if not diff:
        print("(No changes in Formula/specci.rb)")
    else:
        print(diff)


def confirm(prompt: str) -> bool:
    """Simple yes/no confirmation."""
    answer = input(f"{prompt} [y/N]: ").strip().lower()
    return answer in ("y", "yes")


def commit_and_push(version: str) -> None:
    print("\n== Committing and pushing changes ==")
    try:
        run(["git", "add", "Formula/specci.rb"])
        commit_msg = f"Bump specci to v{version}"
        run(["git", "commit", "-m", commit_msg])
        run(["git", "push"])
    except subprocess.CalledProcessError as e:
        print("Error during git add/commit/push.", file=sys.stderr)
        if e.stdout:
            print("--- stdout ---")
            print(e.stdout)
        if e.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
    else:
        print("✅ Changes committed and pushed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update Homebrew formula for specci and optionally commit + push."
    )
    parser.add_argument(
        "version",
        help="Version without 'v' prefix (e.g. 0.1.0). A 'v' will be added for the tag.",
    )
    args = parser.parse_args()

    # Abort if the repo has pending changes (both staged or unstaged)
    try:
        status = run(["git", "status", "--porcelain"], capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to check git status.", file=sys.stderr)
        sys.exit(1)

    if status.stdout.strip():
        print("Error: Your working tree has pending changes.", file=sys.stderr)
        print("Commit or stash them before running publish.py.", file=sys.stderr)
        sys.exit(1)

    ensure_formula_exists()
    update_formula(args.version)
    show_diff()

    if not confirm("\nCommit and push these changes to origin?"):
        print("Aborted. Changes are still in your working tree.")
        sys.exit(0)

    commit_and_push(args.version)


if __name__ == "__main__":
    main()

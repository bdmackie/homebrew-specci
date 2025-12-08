#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

from update_formula import update_formula_https as update_formula_func


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
    """Update the formula using the imported function."""
    print(f"== Updating formula for version {version} ==")
    try:
        update_formula_func(version, FORMULA_PATH)
    except SystemExit as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to update formula: {e}", file=sys.stderr)
        sys.exit(1)


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


def get_tap_name() -> str:
    """Get the tap name from git remote (e.g., bdmackie/specci)."""
    result = run(["git", "remote", "get-url", "origin"], capture_output=True)
    remote = result.stdout.strip()
    
    # Handle both SSH (git@host:owner/repo.git) and HTTPS (https://github.com/owner/repo.git)
    if remote.startswith("git@"):
        parts = remote.split(":")[-1].replace(".git", "")
    elif remote.startswith("https://"):
        parts = remote.split("github.com/")[-1].replace(".git", "")
    else:
        raise ValueError(f"Unknown remote format: {remote}")
    
    owner, repo = parts.split("/", 1)
    # homebrew-specci -> specci
    tap_name = repo.replace("homebrew-", "")
    return f"{owner}/{tap_name}"


def verify_formula_online(version: str) -> None:
    """Verify the formula is updated by checking with brew."""
    print("\n== Verifying formula online ==")
    
    try:
        tap_name = get_tap_name()
    except Exception as e:
        print(f"⚠️  Could not determine tap name: {e}", file=sys.stderr)
        print("   Run manually: brew info specci")
        return
    
    try:
        # Update the tap first to get latest changes
        print(f"Updating tap: {tap_name}")
        run(["brew", "update", tap_name], check=False)
        
        # Get formula info
        print(f"Checking formula version...")
        result = run(["brew", "info", "specci"], capture_output=True, check=False)
        info_output = result.stdout
        
        expected_tag = f"v{version}"
        if expected_tag in info_output:
            print(f"✅ Formula is updated online (tag {expected_tag} found)")
        else:
            # Try to extract tag from output
            tag_match = re.search(r'tag:\s+"([^"]+)"', info_output)
            if tag_match:
                online_tag = tag_match.group(1)
                if online_tag == expected_tag:
                    print(f"✅ Formula is updated online (tag {online_tag})")
                else:
                    print(f"⚠️  Formula shows tag '{online_tag}', expected '{expected_tag}'")
            else:
                print(f"⚠️  Could not verify tag in brew output")
                print("   Run manually: brew info specci")
    except FileNotFoundError:
        print("⚠️  'brew' command not found, skipping online verification")
    except Exception as e:
        print(f"⚠️  Error checking formula: {e}", file=sys.stderr)
        print("   Run manually: brew info specci")


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
        verify_formula_online(version)


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

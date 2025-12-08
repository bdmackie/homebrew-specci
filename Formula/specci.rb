class Specci < Formula
  # Allow overriding the SSH host via environment variable. Defaults to "github-specci".
  HOST = ENV.fetch("SPECCI_GITHUB_HOST", "github-specci")

  # One-line human description
  desc "Specci CLI – spec-driven development helper"

  # Project homepage (GitHub repo is fine to start)
  homepage "https://github.com/bdmackie/specci-client"

  # Build from the git repository via SSH at a specific tag.
  # The SSH host can be overridden with SPECCI_GITHUB_HOST; default is "github-specci".
  url "git@#{HOST}:bdmackie/specci-client.git",
      using: :git,
      tag: "v0.1.0"

  # License identifier
  license "Proprietary"

  # Build-time dependency on Rust/Cargo
  depends_on "rust" => :build

  def install
    # Build and install the CLI from the crates/cli crate
    system "cargo", "install", *std_cargo_args(path: "crates/cli")
end

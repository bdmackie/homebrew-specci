class Specci < Formula
  # Allow overriding the SSH host via environment variable. Defaults to "github-specci".
  HOST = ENV.fetch("SPECCI_GITHUB_HOST", "github-specci")

  # One-line human description
  desc "Specci CLI – spec-driven development helper"

  # Project homepage (GitHub repo is fine to start)
  homepage "https://github.com/bdmackie/specci-client"

  # Build from the git repository via SSH at a specific tag.
  # The SSH host can be overridden with SPECCI_GITHUB_HOST; default is "github-specci".
  url "https://api.github.com/repos/bdmackie/specci-client/tarball/v0.1.2",
      using: :git,
      tag: "v0.1.2"

  # License identifier
  license "Proprietary"

  # Build-time dependency on Rust/Cargo
  depends_on "rust" => :build

  def install
    # Build and install the CLI from the crates/cli crate
    system "cargo", "install", *std_cargo_args(path: "crates/cli")
  end

  test do
    # Smoke test: ensure the binary runs and prints help
    output = shell_output("#{bin}/specci --help")
    assert_match "specci", output
  end
end

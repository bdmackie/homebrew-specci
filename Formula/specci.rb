class Specci < Formula
  # NOTE: This formula file uses HTTPS which is the standard for public repositories.
  # When Specci is released more publicly (either just the releases or the repo is open sourced)
  # we can use this approach.

  # One-line human description
  desc "Specci CLI – spec-driven development helper"

  # Project homepage (GitHub repo is fine to start)
  homepage "https://github.com/bdmackie/specci-client"

  # These two lines are replaced per release using the data from the Python script
  url "https://api.github.com/repos/bdmackie/specci-client/tarball/v0.1.0"
  sha256 "d444cb32aa12a70cea96c75afe7ff3061ff3a1eaa478ad3b467fb04e24f51981"

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

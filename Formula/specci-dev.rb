class SpecciDev < Formula
  HOST = ENV.fetch("SPECCI_GITHUB_HOST", "github-specci")

  # One-line human description
  desc "Specci CLI – spec-driven development helper"

  # Project homepage (GitHub repo is fine to start)
  homepage "https://github.com/bdmackie/specci-client"

  # Build from the git repository via SSH at the head of the main (or dev) branch
  url "git@#{HOST}:bdmackie/specci-client.git",
      using:  :git,
      branch: "main"  # or "dev" if you create a dedicated dev branch

  version "HEAD"
  license "Proprietary"
  depends_on "rust" => :build

  def install
    # Build and install the CLI from the crates/cli crate
    system "cargo", "install", *std_cargo_args(path: "crates/cli")
  end

  test do
    output = shell_output("#{bin}/specci-dev --help")
    assert_match "specci-dev", output
  end
end

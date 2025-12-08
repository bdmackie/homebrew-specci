# Custom download strategy for GitHub API with token support
class GitHubApiDownloadStrategy < CurlDownloadStrategy
  def fetch(timeout: nil, **options)
    token = ENV["SPECCI_CLIENT_GITHUB_TOKEN"] || ENV["HOMEBREW_GITHUB_API_TOKEN"]
    if token
      ohai "Using GitHub token for authentication"
      # Download with curl and Authorization header
      system "curl", "-f", "-L", "-H", "Authorization: Bearer #{token}", url, "-o", cached_location
      raise "Download failed" unless $CHILD_STATUS.success?
    else
      super(timeout: timeout, **options)
    end
  end
end

class Specci < Formula
  # NOTE: This formula file uses HTTPS which is the standard for public repositories.
  # When Specci is released more publicly (either just the releases or the repo is open sourced)
  # we can use this approach.
  #
  # For private repositories, set one of these environment variables before installing:
  #   export HOMEBREW_GITHUB_API_TOKEN="your_github_token_here"
  #   # OR
  #   export SPECCI_CLIENT_GITHUB_TOKEN="your_github_token_here"
  #   brew install specci

  # One-line human description
  desc "Specci CLI – spec-driven development helper"

  # Project homepage (GitHub repo is fine to start)
  homepage "https://github.com/bdmackie/specci-client"

  # These two lines are replaced per release using the data from the Python script
  url "https://api.github.com/repos/bdmackie/specci-client/tarball/v0.1.2",
      using: GitHubApiDownloadStrategy
  sha256 "4942f649df6073eb1e3305234141cf6b1e3ff23e8dd7f8c29c83f0b58f33a2f6"

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

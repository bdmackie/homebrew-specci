class Specci < Formula
    # One-line human description
    desc "Specci CLI – spec-driven development helper"
  
    # Project homepage (GitHub repo is fine to start)
    homepage "https://github.com/bdmackie/specci-client"
  
    # These two lines are replaced per release using the data from the Python script
    url "https://github.com/bdmackie/specci-client/archive/refs/tags/v0.1.0.tar.gz"
    sha256 "ABC123...YOUR_REAL_SHA_HERE..."
  
    # License identifier
    license "MIT"
  
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

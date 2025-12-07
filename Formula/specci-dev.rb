class SpecciDev < Formula
    # Allow overriding the SSH host via environment variable. Defaults to "github-specci".
    HOST = ENV.fetch("SPECCI_GITHUB_HOST", "github-specci")
  
    desc "Specci CLI – dev build from HEAD"
    homepage "https://github.com/bdmackie/specci-client"
  
    # Build from the git repository via SSH at the head of the main (or dev) branch
    url "git@#{HOST}:bdmackie/specci-client.git",
        using:  :git,
        branch: "main"  # or "dev" if you create a dedicated dev branch
  
    # Optional: mark as dev-ish
    version "HEAD"
  
    license "Proprietary"
    depends_on "rust" => :build
  
    def install
      # Build the CLI in release mode from the workspace
      system "cargo", "build", "--release", "--manifest-path", "crates/cli/Cargo.toml"
    
      # Install the resulting binary into Homebrew's bin
      bin.install "target/release/specci"
    end
  
    test do
      output = shell_output("#{bin}/specci --help")
      assert_match "specci", output
    end
  end

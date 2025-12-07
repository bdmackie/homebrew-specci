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
        system "cargo", "install",
               "--locked",
               "--root", prefix,
               "--path", "crates/cli",
               "--force"
    end
  
    test do
      output = shell_output("#{bin}/specci --help")
      assert_match "specci", output
    end
  end

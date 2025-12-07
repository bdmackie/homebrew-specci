# homebrew-specci



## Switching in Development (Mac OS)

If you are developing specci and want to switch between a dev version and the homebrew version, put these scripts into your .zshrc file or similar, ensure ~./bin exists (mkdir if needed), then specci_use_brew / specci_use_cargo to switch.

```sh
# Binary paths
SPECCI_BREW="/opt/homebrew/bin/specci"
SPECCI_CARGO="$HOME/.cargo/bin/specci"
SPECCI_LINK="$HOME/bin/specci"

specci_use_brew() {
  if [ ! -x "$SPECCI_BREW" ]; then
    echo "❌ Homebrew specci not found at $SPECCI_BREW"
    return 1
  fi

  ln -sf "$SPECCI_BREW" "$SPECCI_LINK"
  hash -r  # clear shell command cache
  echo "✅ specci now points to Homebrew: $SPECCI_BREW"
  specci --version 2>/dev/null || true
}

specci_use_cargo() {
  if [ ! -x "$SPECCI_CARGO" ]; then
    echo "❌ Cargo specci not found at $SPECCI_CARGO"
    echo "   Try: cargo install --path crates/cli --force"
    return 1
  fi

  ln -sf "$SPECCI_CARGO" "$SPECCI_LINK"
  hash -r
  echo "✅ specci now points to Cargo: $SPECCI_CARGO"
  specci --version 2>/dev/null || true
}
```

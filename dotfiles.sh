#!/usr/bin/env bash
set -euo pipefail

DOTFILES_REPO="git@github.com:tanaka-mambinge/dotfiles.git"
DOTFILES_DIR="$HOME/.dotfiles"

echo "==> Setting git identity"
git config --global user.name "tanaka-mambinge"
git config --global user.email "tmambingez@gmail.com"

echo "==> Cloning dotfiles repo"
if [ ! -d "$DOTFILES_DIR/.git" ]; then
  git clone "$DOTFILES_REPO" "$DOTFILES_DIR"
else
  echo "Dotfiles repo already exists, pulling latest changes"
  git -C "$DOTFILES_DIR" pull --ff-only
fi

echo "==> Creating symlinks"

# zsh
ln -sf "$DOTFILES_DIR/zshrc" "$HOME/.zshrc"

# opencode
mkdir -p "$HOME/.config/opencode"
ln -sf "$DOTFILES_DIR/opencode.json" \
       "$HOME/.config/opencode/opencode.json"
ln -sf "$DOTFILES_DIR/AGENTS.md" \
       "$HOME/.config/opencode/AGENTS.md"

echo "==> Done"
echo "Restart your shell or run: source ~/.zshrc"

# BreadyX's Utilities (BXU)
The BXUs are some small scrips (mostly bash) that I have written to make my life in Arch Linux a little easier.

These are **simple utilities** and will never be something very complex. Their main goal is to automate repetitive tasks of various nature (system maintenance etc...).

## Requirements:

- Fedora
	- dnf ( even though it should be obvious)
- Flatpak (optional)
- Snap (optional)
- git
- bash

## Installation
It is advised to install these utilities in the user's private bin folder and not system-wide: install in either `$HOME/.local/bin/` or `$HOME/bin` depending on your configuration and preference. The included `install.sh` bash script installs the scripts in `$HOME/.local/bin`. Pass option `--otherbin` to use `$HOME/bin` ($INSTALLDIR).

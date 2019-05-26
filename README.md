# BreadyX's Utilities (BXU)

The BXUs are some small scrips (mostly bash) that I have written to make my life a little easier.

These are **simple utilities** and will never be something very complex. Their main goal is to automate repetitive tasks of various nature.

## Requirements:

- Fedora
- Flatpak (optional)
- Snap (optional)
- git
- posix compliant shell (`bash`, `dash` or others)

## Installation

Run the provided `install.sh` script. By default it will install the scripts in `$HOME/.local/bin/`. The user can also specify another directory by passing the `--otherbin` option. For more information about the usage of the script, please read the output of the `--help` option, which it can also be found here:

```
install.sh [--otherbin path]
This scripts installs the BreadyX's Utils.

By deafult it installs in "$INSTALLDIR", but it can be changed by passing the option --otherbin and giving a path.
```

It is strongly advised to **not** install the scripts in a system-wide bin folder (such as `/usr/local/bin`) for security reasons.

If one doesn't want to use the provided install script, it can simply copy the utilities in the correct folder.

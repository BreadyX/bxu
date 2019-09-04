# BreadyX's Utilities (BXU)

The BXUs are some small scrips that I have written to make my life a little 
easier.

## Requirements:
### General requirements
- Arch Linux (trying to make the scripts the most distro-agnostic possible)
- POSIX compliant shell (`bash`, `dash` or others)
- python for some scripts

### Program specific requirements
- grub (change-boot)
- git (git-hud)

## Installation
### Automated
Run the provided `install.sh` script. By default it will install the scripts in
`$HOME/.local/bin/`. The user can also specify another directory by passing the
`--otherbin` option. 

[//]: # It is strongly advised to **not** install the scripts in a system-wide bin 
[//]: # folder (such as `/usr/local/bin`) for security reasons.

### Manual
Copy all scripts inside the project directory into a folder of your choice and
add it to your PATH.

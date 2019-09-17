# BreadyX's Utilities (BXU)

The BXUs are some small scrips that I have written to make my life a little 
easier.

## Requirements:
### General requirements
- Arch Linux (trying to make the scripts the most distro-agnostic possible)
- POSIX compliant shell (`bash`, `dash` or others)

### Program specific requirements
- grub (change-boot)
- git (git-hud)
- python (clean)
- awk (clean)

## Installation
### Automated
Run the provided `install.sh` script. By default it will install the scripts in
`$HOME/.local/bin/`. The user can also specify another directory by passing the
`--otherbin` option. 

### Manual
Copy all executables inside the `utils` directory into a folder of your choice and
add that folder to your PATH.

## Contents
Here's a run-through of all of the scripts and their functionality. I remind you
that all the information can be found inside the help dialog of each program
(`--help` option).

# WIP from here onwards

### change-boot (sh)
`change-boot` is a shell script that lets you change your default grub entry
by changing the `GRUB_DEFAULT` option in the grub config file for you with the
correct value.

- Syntax: `change-boot [TYPE|OPTION]`
- TYPEs:
	- `linux`: the default kernel
	- `linux-lts`: the long term support kernel
- OPTIONs:
	- `--info`: show info about installed kernels
	- `--help`: show help dialog
	- `--version`: show version info

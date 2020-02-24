# BreadyX's Utilities (BXU)
The BXU's are small programs, of various complexity, that I have written to make
my life a little easier. The utilities are designed for a GNU/Linux system. 
However they could still function on other *NIX system (MacOS, *BSD).

The repo is subdivided in multiple 'subprojects'. More info on each subproject
can be found in the respective directories.

## Requirements
Every program requires the **meson build system**.

The dependencies marked in **bold** are build time dependencies
| Project      | Dependency            |
|--------------|-----------------------|
| git-hud      | python3, git          |
| ic           | python3, gcc          |
| laptop-stuff | NetworkManager, nmcli |
| confs\*      | --                    |

\*Still in development. Avoid if you want

## Installation
### Automated
Run the `install.sh` script from the root of the project. You can use
its options to tweak the behaviour to you liking

Help dialog for `install.sh`:
```
install.sh [ OPTIONS ]
Installs the BreadyX's Utils.

Options:
    -p, --prefix=PATH   Use this install directory instead of default
	-x, --exclude=PROJ  Do not install these projects (comma separated)
	-l, --list			List all installable projects and exit
    -h, --help          Display this message and exit
```

#### Examples:
```sh
# Install every project into $HOME/mydir
./install.sh -p $HOME/mydir
# Install every project except `project` in default directory 
./install.sh -x project
```

### Manual
If you want to do things manually go into each project directory and build it 
manually with meson:
```sh
# Example with git-hud
cd ./src/git-hud
# Setup build dir for installation in $HOME/.local/ and install
meson ./build --prefix="$HOME/.local" 
ninja -C ./build install
```

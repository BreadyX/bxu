#! /bin/sh
# To be sourced by `install.sh`. First argument is INSTALLDIR

cp -u ./git-hud "$1/" || {
    echo "ERROR: couldn't copy file: have you checked permissions?"
    exit 1
}

### If user has write permissions (checked previously) he can also change
### properties
chmod +x "$1/git-hud"


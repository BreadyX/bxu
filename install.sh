#!/bin/sh -e

DOC="install.sh [--otherbin path]
This scripts installs the BreadyX's Utils.

By default it installs in '$INSTALLDIR', but it can be changed by passing the
option --otherbin and giving a path."
INSTALLDIR="$HOME/.local/bin"
PROJS="$(for dir in $(find src/ -type d | grep -v 'src/$'); do basename "$dir"; done)"

ERRORS=0

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --otherbin)
            printf "Setting install directory to %s\n" "$2"
            INSTALLDIR="$(realpath "$2")"
            shift 2 ;;
        "")
            ;;
        --help|*)
            printf "%s\n" "$DOC"
            exit 0 ;;
    esac
done

# Prompt user
printf "This script will install the BreadyX utils (BXU) inside %s\nProceed? [y/n] " "$INSTALLDIR"
read -r i
if [ "$(echo "$i" | tr "[:upper]" "[:lower]")" = "n" ]; then
	printf "Aborted by user\n"
	exit 0
fi

# Check for directory
if ! { [ -d "$INSTALLDIR" ] || [ -w "$INSTALLDIR" ]; } ; then
	printf "Cannot access %s: directory doesn't exists or user hasn't access to it\n"\
        "$INSTALLDIR"
	exit 1
fi

# Loop projects and run `setup.sh` in a subshell
for proj in $PROJS; do
    proj_dir="./src/$proj"
    printf "Installing '%s':\n" "$proj_dir"
    if [ -d "$proj_dir" ]; then
        if [ -f "$proj_dir/setup.sh" ] && [ -x "$proj_dir/setup.sh" ]; then
            ( cd "$proj_dir"
              sh setup.sh "$INSTALLDIR" | fold | sed 's/^/\t/'
            ) || { printf "\tError in setup of %s\n" "$proj"; $((ERRORS++)); }
              && printf "\tDone\n"
        else
            printf "\tMissing setup for project '%s'. Please file an issue\n" "$proj"
        fi
    else
        printf "\tMissing project '%s'. Please file an issue\n" "$proj"
    fi
    printf "\n"
done

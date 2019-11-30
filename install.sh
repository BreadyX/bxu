#!/bin/sh -e

INSTALLDIR="$HOME/.local/bin"
PROJS="clean confs git-hud ic laptop-stuff"

# Parse arguments
case "$1" in
	--otherbin)
		printf "Setting install directory to %s\n" "$2"
		INSTALLDIR="$2" ;;
    "")
        ;;
	--help|*)
		cat << EOF
install.sh [--otherbin path]
This scripts installs the BreadyX's Utils.

By deafult it installs in "$INSTALLDIR", but it can be changed by passing the
option --otherbin and giving a path.
EOF
		exit 0 ;;
esac

# Prompt user
printf "This script will install the BreadyX utils (BXU) inside %s\nProceed? [y/n] " "$INSTALLDIR"
read -r i
[ "$(echo "$i" | tr "[:upper]" "[:lower]")" = "n" ] && {
	printf "Aborted by user\n"
	exit 0
}

# Check for directory
[ -d "$INSTALLDIR" ] || {
	printf "Directory %s doesn't exists. Please create it\n" "$INSTALLDIR"
	exit 1
}

# Loop projects and run `setup.sh` in a subshell
for proj in $PROJS; do
    printf "Installing '%s':\n" "$proj"
    if [ -d "$proj" ]; then
        if [ -f "$proj/setup.sh" ]; then
            (
                cd "$proj"
                sh setup.sh "$INSTALLDIR" | fold | sed 's/^/\t/'
            )
        else
            printf "\tMissing setup for project '%s'. Please file an issue\n" "$proj"
        fi
    else
        printf "\tMissing project '%s'. Please file an issue\n" "$proj"
    fi
    printf "\n"
done

# get files
# files="$(find ./utils/ -type f | tr "\n" " ")"

# Make file executables if they are not
# chmod +x $files

# Copy files to INSTALLDIR
# cp -ui $files "$INSTALLDIR"

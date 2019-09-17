#!/bin/sh -e

INSTALLDIR="$HOME/.local/bin"

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
	printf "Directory %s doesn't exists. Please first create it and then try reinstalling." "$INSTALLDIR"
	exit 1
}

# Remove unwanted files
files="$(ls -a | grep -Ev "(^\.|deprecated|install\.sh|README)" | tr '\n' ' ')"

# Make file executables if they are not
chmod +x $files

# Copy files to INSTALLDIR
cp -i $files "$INSTALLDIR"

#!/bin/bash

if [ "$1" == "--otherbin" ]; then INSTALLDIR="$HOME/bin"
else INSTALLDIR="$HOME/.local/bin"; fi # choose directory based on input

echo "This script will install the BreadyX utils (BXU) inside $USER's local bin folder ($INSTALLDIR)"

read -rp "Proceeed? [Y/n] " input
[ "${input,,}" == "n" ] && { echo "Aborted by user"; exit 0; }

### install into .local/bin/
chmod +x ./* # Make file executables if they are not
eval "mkdir -p $INSTALLDIR" &> /dev/null # Prepare directory

cp -r ./* "$INSTALLDIR" # Copy file
rm "$INSTALLDIR/README.md" "$INSTALLDIR/install.sh" # Cleanup
rm -rf "$INSTALLDIR/Deprecated" "$INSTALLDIR/.git" # Cleanup

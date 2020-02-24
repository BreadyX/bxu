#!/bin/bash -e

PREFIX="$HOME/.local/"
BUILDDIR="./meson-build"
PROJS="$(
	for dir in $(find ./src/ -maxdepth 1 -type d | grep -v 'src/$'); do
		basename "$dir"
	done
)"
EXCLUDE=""

DOC="install.sh [ OPTIONS ]
Installs the BreadyX's Utils.

Options:
    -p, --prefix=PATH   Use this install directory instead of default
    -x, --exclude=PROJ  Do not install these projects (comma separated)
    -l, --list          List all installable projects and exit
    -h, --help          Display this message and exit"

RED="$(tput setaf 1)"
GREEN="$(tput setaf 2)"
YELLOW="$(tput setaf 3)"
GRAY="$(tput setaf 250)"
BOLD="$(tput bold)"
RESET="$(tput sgr0)"

ARGS=$(getopt -n "install.sh" -o "hlp:x:" -l "help,list,prefix:,exclude:" -- "$@")
set -- $ARGS
while true; do
	case $1 in
		-h|--help)
			printf "%s\n" "$DOC"
			exit 0 ;;
		-p|--prefix)
			shift
			PREFIX="$(echo $1 | xargs)"
			shift ;;
		-l|--list)
			shift
			printf "%s\n" "$PROJS"
			exit 0 ;;
		-x|--exclude)
			shift
			read -a EXCLUDE -r < <(echo "$1" | sed "s/,/ /g" | xargs)
			shift ;;
		--)
			shift
			break ;;
	esac
done

printf "The BreadyX utils (BXU) will be installed in %s\n" "$PREFIX/*"
printf "Proceed? [Y/n]"
read -r i
if [ "$(echo "$i" | tr "[:upper]" "[:lower]")" = "n" ]; then exit 0; fi

for proj in $PROJS; do
	printf "\n"

	# esoteric way to check is $proj is in EXCLUDE. This is necessary as bash's
	# arrays are quite a PITA
	if [ "$EXCLUDE" != "${EXCLUDE#$proj}" ]; then continue; fi

	proj_dir="./src/$proj"
	printf "%sInstalling %s:%s\n" "$BOLD" "$proj" "$RESET"
	if [ -f "$proj_dir/meson.build" ]; then
		out="$(
			cd "$proj_dir"
			if [ -d "$BUILDDIR" ]; then
				meson "$BUILDDIR" --reconfigure --prefix="$PREFIX" --buildtype=release
			else
				meson "$BUILDDIR" --prefix="$PREFIX" --buildtype=release
		  	fi
		  	ninja -C "$BUILDDIR" install
		)"
		exit_code=$?
		printf "%s%s%s\n" "$GRAY" "$out" "$RESET" | sed "s/^/\t/"
		if [ "$exit_code" == 0 ]; then
			printf "\t%sDone%s\n" "$GREEN" "$RESET"
		else
			printf "\t%sError%s\n" "$RED" "$RESET"
		fi
	else
		printf "\t%sMissing setup for %s%s\n" "$YELLOW" "$proj" "$RESET"
	fi
done

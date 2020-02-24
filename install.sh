#!/bin/bash -e

INSTALLDIR="$HOME/.local/bin"
PROJS="$(for dir in $(find src/ -maxdepth 1 -type d | grep -v 'src/$'); do basename "$dir"; done)"
EXCLUDE=""
DOC="install.sh [ OPTIONS ]
Installs the BreadyX's Utils.

    -b, --bin=PATH      Use this install directory instead of default
	-x, --exclude=PROJ  Do not install these projects (comma separated)
	-l, --list			List all installable projects and exit
    -h, --help          Display this message and exit"

RED="$(tput setaf 1)"
GREEN="$(tput setaf 2)"
YELLOW="$(tput setaf 3)"
GRAY="$(tput setaf 250)"
BOLD="$(tput bold)"
RESET="$(tput sgr0)"

ARGS=$(getopt -n "install.sh" -o "hlb:x:" -l "help,list,bin:,exclude:" -- "$@")
set -- $ARGS
while true; do
	case $1 in
		-h|--help)
			printf "%s\n" "$DOC"
			exit 0 ;;
		-b|--bin)
			shift
			INSTALLDIR="$(echo $1 | xargs)"
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

printf "This script will install the BreadyX utils (BXU) inside %s\nProceed? [y/n] " "$INSTALLDIR"
read -r i
if [ "$(echo "$i" | tr "[:upper]" "[:lower]")" = "n" ]; then
	printf "Aborted by user\n"
	exit 0
fi
printf "\n"

if { ! [ -d "$INSTALLDIR" ]; } && { ! [ -w "$INSTALLDIR" ]; } ; then
	printf "Cannot access %s: directory doesn't exists or user hasn't access to it\n"\
		"$INSTALLDIR"
	exit 1
fi

for proj in $PROJS; do
	proj_dir="./src/$proj"
	if [ "$EXCLUDE" != "${EXCLUDE#$proj}" ]; then # proj is in EXCLUDE
		continue
	fi
	printf "%sInstalling '%s':%s\n" "$BOLD" "$proj" "$RESET"
	if [ -x "$proj_dir/setup.sh" ]; then
		( set +e
		  cd "$proj_dir"
		  out="$(sh -e setup.sh "$INSTALLDIR")" exit_code=$?
		  printf "%s%s%s\n" "$GRAY" "$out" "$RESET" | fold | sed 's/^/\t/'
		  if [ "$exit_code" != 0 ]; then
			   printf "\t%sError in setup of %s%s\n" "$RED" "$proj" "$RESET"
			   exit 1
		  fi ) && printf "\t%sDone%s" "$GREEN" "$RESET"
	else
		printf "\t%sMissing setup for project '%s'%s\n" "$YELLOW" "$proj" "$RESET"
	fi
	printf "\n"
done

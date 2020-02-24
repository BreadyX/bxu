# Called by install.sh
# First parameter is INSTALLDIR, cwd is ./src/laptop-stuff

cp -u --preserve=mode ./toggle-wifi "$1/" >/dev/null 2>&1 || {
	echo "Error: couldn't copy file"
	exit 1
}

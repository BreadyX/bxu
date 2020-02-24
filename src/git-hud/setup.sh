# Called by `install.sh`.
# First argument is INSTALLDIR, cwd is ./src/git-hud

prefix="$(dirname $1)"
if [ -d './meson-build' ]; then
	meson "./meson-build" --reconfigure --prefix="$prefix"
else
	meson "./meson-build" --prefix="$prefix"
fi

ninja -C "./meson-build" install


# bat-hud
Small python script that formats a quick summary about the charge of the
battery (if available) and ouptuts it to standard output.

If the environment variable `BAT_HUD_GLYPH` is set, the script will use
unicode glyphs. The variable is always ignored if a tty is detected.

`bat-hud` help dialog:
```
usage: bat-hud [-h] [-v]

Format a quick summary about the cnarge of the battery, if available.

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show info about version

If the environment variable BAT_HUD_GLYPH is set, the script will use unicode
glyphs. The variable is, however, ignored if a tty is used.
```

## Dependencies
- meson
- python3
- fontawesome (if used with `BAT_HUD_GLYPH`)

## Use and Features
Designed to be used inside a prompt (like a shell prompt). It shows only essential
information in a very short and compact format

Information shown:
- Charge percent
- Battery status (charging or discharging)

## Example
With `BAT_HUD_GLYPH` set: ` 99%`  
Without `BAT_HUD_GLYPH` set: `Charging: 99%`

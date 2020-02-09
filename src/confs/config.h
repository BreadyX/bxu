#ifndef CONFIG_H	// CONFIG_H
#define CONFIG_H

#define VERSION @version@
#define CONFIG_SEARCH "/etc/bsnap/bsnap.conf:~/.config/bsnap/bsnap.conf"
char DB_DIR[256] = "~/.local/share/bsnap";
int  CHUNK_SIZE = 16384;

#endif


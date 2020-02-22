#include <stdio.h>
#include <string.h>
#include <getopt.h>

#include "config.h"

#define FIRST_LEVEL_CMD "+:hvc:d:"

int main(int argc, char** argv)
{
	int opt;
	
	opterr = 0; // no error output
	while ((opt = getopt(argc, argv, FIRST_LEVEL_CMD)) != -1) {
		switch (opt) {
			case 'h': printf("Help\n"); return 0;
			case 'v': printf("Version\n"); return 0;
			case 'c': printf("Using config %s\n", optarg); break;
			case 'd': printf("Using db path %s\n", optarg); break;
			case '?': printf("Invalid option %c\n", optopt); return 1;
			case ':': printf("Missing argument from %c\n", optopt); return 1;
		}
	}
	// arrived at second level: TODO optimize beacuse is shitty
	printf("%d %d\n", optind, argc);
	if (optind == argc) { // no action
		printf("What do you want me to do?\n");
		return 1;
	}
	if (strcmp(argv[optind], "snap") == 0) { //snap
		if (argc - optind == 1)
			printf("Snapping everything\n");
		else
			printf("Snapping %s\n", argv[optind + 1]);
		return 0;
	} else if (strcmp(argv[optind], "restore") == 0) { //restore
		if (argc - optind == 1) {
			printf("What do I restore?\n");
			return 1;
		} else if (argc - optind >= 2) { // is ok
			printf("Restoring %s ", argv[optind + 1]);
			if (argc - optind == 3)
				printf("to %s", argv[optind + 2]);
			printf("\n");
			return 0;
		}
	}

}

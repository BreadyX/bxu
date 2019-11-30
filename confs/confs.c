#include <stdio.h>
#include <stdbool.h>
#include <getopt.h>

bool EDIT = false;

#define OPTSTRING "+hvceEV"
#define ACTION_EXIT 0
#define ACTION_EDIT 1
#define ACTION_VIEW 2
#define EMPTY_ARG {0, 0, 0, 0}

int ACTION = 0;
struct option LONG_OPTS[] = {
    { "help", no_argument, &ACTION, ACTION_EXIT },
    { "version", no_argument, &ACTION, ACTION_EXIT },
    { "config", required_argument, NULL, 'c' },
    { "editor", required_argument, NULL, 'e' },
    { "edit", no_argument, &ACTION, ACTION_EDIT },
    { "view", no_argument, &ACTION, ACTION_VIEW },
    EMPTY_ARG
};

int main(int argc, char** argv)
{
    char current_contex_opts[15];
    int arg_ev = 1,
        getopt_return;

    opterr = 0; // turnoff getopt error
    if (argc == 1)
        return 1;
    while (arg_ev < argc) {
        getopt_return = getopt(argc, argv, OPTSTRING);
        switch(getopt_return) {
            case 'h':
                printf("Help\n");
                break;
            case '?':
                return 1;
            default:
                return 0;
        }
        /* printf("%d %c\n", getopt_return, getopt_return); */
        arg_ev++;
    }

    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
// #include <unistd.h>
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
        arg_ev++;
    }

    return 0;
}

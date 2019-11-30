#! /usr/bin/env python3
"""Cleans directories of files based on specified patterns."""

import os
import re
import sys
import getopt
import textwrap
from subprocess import check_output

### Program info
NAME = 'clean'
VERSION = '1.99.0'
SYNTAX = f'Usage: {NAME} [ OPTION ]... [ PATTERNS ]...'
OVERVIEW = ('Cleans a directory based on specified patterns. If PATTERNS are '
            'not specified, the script will search DIRECTORY for a file named '
            "'cleanfile'. Each pattern is treated as an extended regular "
            'expression.')

### OPTIONS
OPTIONS = {'file':      ('-F:', '--file=', '',
                         'Specify cleanfile to read if no patterns are given'),
           'directory': ('-D:', '--directory=', '', 'The directory to clean'),
           'ask':       ('-a', '--ask', 'ask',
                         'Ask for confirmation before removal'),
           'dry':       (' ', '--dry-run', '', 'Only print the actions'),
           'rm-dir':    ('-d', '--rm-dir', 'rm-dir',
                         'Also remove directories'),
           'recursive': ('-r', '--recursive', 'recursive',
                         'Recurse into subdirectories'),
           'verbose':   ('-v', '--verbose', 'verbose', 'Be verbose'),
           'help':      ('-h', '--help', '', 'Print this dialog'),
           'version':   ('-V', '--version', '', 'Print dialog about version')}

### OPTIONS access
SHORT = 0
LONG = 1
CLEANFILE_FLAG = 2
DESC = 3

### CLEANFILE info
CLEANFILE_FLAGS = [o[CLEANFILE_FLAG] for o in OPTIONS.values()
                   if o[CLEANFILE_FLAG]]
ADDITIONAL_INFO = (("A 'cleanfile' is a plain text file containing the "
                    "patterns to use separated by space, horizontal tab, "
                    "newline or a combination of them. Comments are supported "
                    "and are delimited by '#'.  Everything after '#' until a "
                    "newline is considered a comment. By beginning the first "
                    "line of the file with '#F:' some flags can be set to "
                    "either 0 (disabled) or 1 (enabled). The flags must be "
                    "separated by a whitespace."),
                   f'Available flags: {" ".join(CLEANFILE_FLAGS)}')

### Regexes
CLEANFILE_FLAGS_REGEX = re.compile(f'({"|".join(CLEANFILE_FLAGS)})=([0-1])')
CLEANFILE_LINE_CLEAN_REGEX = re.compile(r'(#.*$)|(\s*$)|(^\s*)')
### Usage: [ p for p in re.split("( |\\\".*?\\\"|'.*?')", a) if p.strip()]
CLEANFILE_LINE_SPLIT_REGEX = re.compile(r"( |\\\".*?\\\"|'.*?')")

### DEFAULTS
DEFAULT_OPTS = {'file':      '',
                'directory':  './',
                'ask':        False,
                'dry':        False,
                'rm-dir':     False,
                'recursive':  False,
                'verbose':    False}

def main():
    """Main function"""
    cli_options, cli_patterns = eval_argv(sys.argv[1:])
    options = eval_options(cli_options)
    compiled_pattern = None
    if not options:  # check for no options (help or version)
        return
    if options['directory'] != DEFAULT_OPTS['directory']:
        if not os.path.isdir(options['directory']):
            raise ValueError(f'{options["directory"]} is not a valid '
                             'directory')
    if cli_patterns:
        compiled_pattern = compile_patterns(cli_patterns)
    else:  # look for cleanfile
        if options['file'] != DEFAULT_OPTS['file']:
            if not os.path.isfile(options['file']):
                raise ValueError(f'cleanfile {options["file"]} is not a valid '
                                 'file')
        else:
            options['file'] = find_cleanfile(options['directory'])
        # cleanfile flags
        compiled_pattern = compile_cleanfile_patterns(options['file'])
    # if verbose: print init
    # get dir info
    # if recursive:
    #       clean recursively
    #       if rmdir:
    #           clean recursively dirs
    #       else:
    # else
    #       clean
    #       if rmdir:
    #           clean dirs


def eval_argv(argv):
    """Parse argv and return options and arguments"""
    short = ''.join([s[SHORT][1:] for s in OPTIONS.values()])
    long = [l[LONG][2:] for l in OPTIONS.values()]
    try:
        return getopt.getopt(argv, short, long)
    except getopt.GetoptError as err:
        raise RuntimeError(str(err))


def eval_options(cli_options):
    """Return options based on cli_options"""
    options = DEFAULT_OPTS.copy()
    for option, value in cli_options:
        if option in (OPTIONS['help'][0], OPTIONS['help'][1]):
            print(make_dialog('H'))
            return None
        if option in (OPTIONS['version'][0], OPTIONS['version'][1]):
            print(make_dialog('V'))
            return None
        for short, long, _, _ in OPTIONS.values():
            if option in (short[0:2], long[0:-1]):
                if long[-1] == '=':
                    options[long[2:-1]] = value
                else:
                    options[long[2:]] = True
    return options

def make_dialog(typ):
    """Construct help and version dialogs"""
    dialog = ''
    if typ == 'H':
        dialog += SYNTAX + '\n' * 2  # add syntax
        dialog += textwrap.fill(OVERVIEW, 80) + '\n' * 2  # add overview
        for short, long, _, description in OPTIONS.values():  # add options
            dialog += f'\t{short[0:2]:2}, {long}\t{description}\n'
        for info in ADDITIONAL_INFO:  # add additional info
            dialog += '\n'
            dialog += textwrap.fill(info, 80) + '\n'
    elif typ == 'V':
        dialog = (f'{NAME} - BreadyX\'s utils. Version {VERSION}.'
                  'Written bt BreadyX.\n\tContacts:\n'
                  'https://github.com/BreadyX/bxu')
    else:
        raise ValueError(f'Invalid type {typ}')
    return dialog


def compile_patterns(patterns):
    raise NotImplementedError()


def compile_cleanfile_patterns(cleanfile_path):
    raise NotImplementedError()


def find_cleanfile(directory):
    raise NotImplementedError()


if __name__ == '__main__':
    try:
        if os.geteuid() == 0:
            print('RUNNING WITH ROOT PRIVILEGES. BE CAREFUL!')
            input('Press any key to continue...')
        main()
    except (RuntimeError, ValueError) as error:
        RED = "\033[31m"
        RESET = "\033[0m"
        if os.environ.get('CLEAN_DEBUG'):
            raise error
        print(f'{RED}Error: {str(error)}{RESET}. Use {NAME} '
              f'{OPTIONS["help"][LONG]} for more info.')
        exit(1)

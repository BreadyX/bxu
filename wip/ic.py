#! /usr/bin/env python3
"""interactive c"""
import sys
import os
import tempfile

WELCOME_STR = "Welcome! Type '{}' for help."
GOODBY_STR = "Goodbye!"
CMD_ERR = "Invalid command '{}', see {} for more info"

STD_H = ('<stdio.h>', '<stdlib.h>')
STD_F = (["int main(int argc, char **argv)", ''],)

ALIVE = 1
USER_INPUT = 2
COMMAND = 3
ARGUMENT = 4
HEADERS = 5
MACROS = 6
FUNCTIONS = 7

def main():
    """main"""
    context = {ALIVE: True,
               USER_INPUT: '',
               COMMAND: '',
               ARGUMENT: '',
               HEADERS: list(STD_H),
               MACROS: [],
               FUNCTIONS: list(STD_F),
               }
    welcome()

    while context[ALIVE]:
        try:
            context[USER_INPUT] = input("> ")
        except EOFError:
            print('')  # Maintain good alignment
            context[ALIVE] = False
            context[USER_INPUT] = ''
        context[USER_INPUT] = context[USER_INPUT].strip()
        if context[USER_INPUT]:
            context[COMMAND] = context[USER_INPUT].split(sep=' ')[0]
            context[ARGUMENT] = context[USER_INPUT][len(context[COMMAND]):].strip()
            cmd_func = CMDS.get(context[COMMAND], None)
            try:
                cmd_func(context)
            except TypeError:
                print(CMD_ERR.format(context[COMMAND], '?'))
            # cmd_func(context)

    goodbye()

def welcome():
    """welcome"""
    print(WELCOME_STR.format('?'))

def goodbye():
    """goodbye"""
    print(GOODBY_STR)

def help_dialog(_):
    """Print information about commands"""
    print("Command\t\tDescription\n" + 100*'-')
    for cmd in CMDS:
        print(f'{cmd}\t\t{CMDS[cmd].__doc__}')

def exit_program(context):
    """Quits program"""
    context[ALIVE] = False

def add_header(context):
    """Add argument to imported headers (<> and "" required)"""
    if context[ARGUMENT] not in context[HEADERS]:
        context[HEADERS].append(context[ARGUMENT])
    else:
        print("Header already imported")

def clear_headers(context):
    """Reset all headers to standard"""
    context[HEADERS].clear()
    context[HEADERS] = list(STD_H)

def list_headers(context):
    """List all added headers"""
    print("Defined headers:")
    for header in context[HEADERS]:
        print(f'\t#include {header}')

def add_macro(context):
    """Define macro matching the argument if not already defined (multiline not supported)"""
    if context[ARGUMENT] not in context[MACROS]:
        context[MACROS].append(context[ARGUMENT])
    else:
        print("Macro already defined")

def clear_macros(context):
    """Delete all user defined macros"""
    context[MACROS].clear()

def list_macros(context):
    """List all added macros"""
    print("Defined macros:")
    for macro in context[MACROS]:
        print(f'\t#define {macro}')

def mod_with_editor(original):
    """Modify `original` string into an editor buffer and return the result"""
    tmp_name = ''
    new = ''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as wtmp:
        tmp_name = wtmp.name
        wtmp.write(original)
    if os.environ["EDITOR"]:
        os.system(f"{os.environ['EDITOR']} {tmp_name}")
    else:
        os.system(f"vi {tmp_name}")
    with open(tmp_name, 'r') as rtmp:
        new = rtmp.read()
    os.remove(tmp_name)
    return new


def add_func(context):
    """Create a new function with given function protoype"""
    to_create = None

    if context[ARGUMENT] == 'main':
        to_create = context[FUNCTIONS][0]  # main is always first
    else:
        for func in context[FUNCTIONS]:
            if context[ARGUMENT] == func[0]:
                to_create = func
                break
    if not to_create:
        to_create = [context[ARGUMENT], '']
        context[FUNCTIONS].append(to_create)
    to_create[1] = mod_with_editor(to_create[1])


def clear_funcs(context):
    """Reset all functions to standard"""
    context[FUNCTIONS].clear()
    context[FUNCTIONS] = list(STD_F)

def list_funcs(context):
    """List all declared functions"""
    to_p = ''
    print("Defined functions:")
    for func in context[FUNCTIONS]:
        to_p = '\t' + func[0] + ' - '
        to_p = to_p + 'Body defined' if func[1] else to_p + 'Body not defined'
        print(to_p)

def merge(headers, macros, functions):
    """Builds a C file with the specified components and returns its path"""
    raise NotImplementedError

def build(doc, delete=False):
    """Compiles specified C file and returns the executable path"""
    raise NotImplementedError

def run(out):
    """Runs specified executable"""
    raise NotImplementedError

def execute(context):
    """Build and execute resulting file"""
    doc = merge(context[HEADERS], context[MACROS], context[FUNCTIONS])
    out = build(doc)
    run(out)
    os.remove(doc)
    os.remove(out)

def check(context):
    """Check resulting program for errors"""
    doc = merge(context[HEADERS], context[MACROS], context[FUNCTIONS])
    build(doc, delete=True)
    os.remove(doc)

def preview(context):
    """Show preview of merged file"""
    doc = merge(context[HEADERS], context[MACROS], context[FUNCTIONS])
    print("Document:\n" + 100*'-')
    for line in doc:
        print(line)
    os.remove(doc)

if __name__ == '__main__':
    CMDS = {'?': help_dialog,
            'help': help_dialog,
            'exit': exit_program,
            'quit': exit_program,

            'addh': add_header,
            'clh' : clear_headers,
            'llh' : list_headers,

            'defm': add_macro,
            'clm' : clear_macros,
            'llm' : list_macros,

            'deff': add_func,
            'clf' : clear_funcs,
            'llf' : list_funcs,

            # 'vim' : None,

            'prev': None,
            'chk' : None,
            'exec': None,
            }
    try:
        main()
    except KeyboardInterrupt:
        goodbye()

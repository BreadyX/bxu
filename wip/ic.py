#! /usr/bin/env python3
"""interactive c"""
import sys
import os
import tempfile
# import functools

WELCOME_STR = "Welcome! Type '{}' for help."
GOODBY_STR = "Goodbye!"
CMD_ERR = "Invalid command '{}', see {} for more info"

STD_H = ('<stdio.h>', '<stdlib.h>')
STD_F = (["int main(int argc, char **argv)", ''],)

ALIVE = 1
CMDS = 2
USER_INPUT = 3
USER_COMMAND = 4
USER_ARGUMENT = 5
HEADERS = 6
MACROS = 7
GLOBALS = 8
FUNCTIONS = 9

def main(argv):
    """main"""
    context = {ALIVE: True,
               CMDS: {'?': help_dialog,
                      'help': help_dialog,
                      'exit': exit_program,
                      'quit': exit_program,

                      'addh': add_header,
                      'modh': None,
                      'clh' : clear_headers,
                      'llh' : list_headers,

                      'defm': add_macro,
                      'modm': None,
                      'clm' : clear_macros,
                      'llm' : list_macros,

                      'addg': add_global,
                      'modg': None,
                      'clg' : clear_globals,
                      'llg' : list_globals,

                      'deff': add_func,
                      'clf' : clear_funcs,
                      'llf' : list_funcs,

                      'prev': None,
                      'chk' : None,
                      'exec': None,},
               USER_INPUT: '',
               USER_COMMAND: '',
               USER_ARGUMENT: '',
               HEADERS: [],
               MACROS: [],
               GLOBALS: [],
               FUNCTIONS: [],}
    # Greet
    print(WELCOME_STR.format('?'))
    # INIT
    clear_list(context[HEADERS], STD_H)
    clear_list(context[FUNCTIONS], STD_F)
    # Parse argv
    # ...
    # Loop and prompt
    while context[ALIVE]:
        try:
            context[USER_INPUT] = input("> ").strip()
        except EOFError:
            print('')  # Maintain good alignment
            context[ALIVE] = False
            context[USER_INPUT] = ''
        if context[USER_INPUT]:
            context[USER_COMMAND] = context[USER_INPUT].split(sep=' ')[0]
            context[USER_ARGUMENT] = context[USER_INPUT][len(context[USER_COMMAND]):].strip()
            cmd_func = context[CMDS].get(context[USER_COMMAND], None)
            try:
                cmd_func(context)
            except TypeError:
                print(CMD_ERR.format(context[USER_COMMAND], '?'))
    # Greet
    print(GOODBY_STR)

def help_dialog(context):
    """Print information about commands"""
    doc = ''
    print("Command\t\tDescription\n" + 100*'-')
    for cmd in context[CMDS]:
        doc = 'N.A.' if not context[CMDS][cmd].__doc__ else context[CMDS][cmd].__doc__
        print(f'{cmd}\t\t{doc}')

def exit_program(context):
    """Quits program"""
    context[ALIVE] = False

def add_to(the_list, arg):
    """Add to index in context"""
    if arg not in the_list:
        the_list.append(arg)
    else:
        print("Already present")

def clear_list(the_list, standard=None):
    """Clears list in context[index]. If standard is not None, reinits the list
    to it"""
    the_list.clear()
    if standard:
        for std in standard:
            the_list.append(std)

def choose_between(the_list):
    """Print a list and let the user choose. Return the index of the chosen item"""
    user_in = None
    for i, val in enumerate(the_list):
        print(f'{i} {val}')
    try:
        user_in = int(input("?> "))
    except ValueError:
        return -1
    if (user_in < 0 or user_in >= len(the_list)):
        return -1
    return user_in

def add_header(context):
    """Add argument to imported headers (<> and "" required)"""
    add_to(context[HEADERS], context[USER_ARGUMENT])

def clear_headers(context):
    """Reset all headers to standard"""
    clear_list(context[HEADERS], STD_H)

def list_headers(context):
    """List all added headers"""
    print("Defined headers:")
    for header in context[HEADERS]:
        print(f'\t#include {header}')

def add_macro(context):
    """Define macro matching the argument (multiline not supported)"""
    add_to(context[MACROS], context[USER_ARGUMENT])

def clear_macros(context):
    """Delete all user defined macros"""
    clear_list(context, MACROS)

def list_macros(context):
    """List all added macros"""
    print("Defined macros:")
    for macro in context[MACROS]:
        print(f'\t#define {macro}')

def add_global(context):
    """Add argument to globals"""
    add_to(context[GLOBALS], context[USER_ARGUMENT])

def clear_globals(context):
    """Clear all defined globals"""
    clear_list(context, GLOBALS)

def list_globals(context):
    """List all defined globals"""
    print("Defined globals:")
    for glob in context[GLOBALS]:
        print(f"\t{glob}")

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
    """Create/modify a function with given function protoype"""
    to_create = None

    if not context[USER_ARGUMENT]:
        print("No prototype")
        return
    elif context[USER_ARGUMENT] == 'main':
        to_create = context[FUNCTIONS][0]  # main is always first
    else:
        for func in context[FUNCTIONS]:
            if context[USER_ARGUMENT] == func[0]:
                to_create = func
                break
    if not to_create:
        to_create = [context[USER_ARGUMENT], '']
        context[FUNCTIONS].append(to_create)
    to_create[1] = mod_with_editor(to_create[1])

def clear_funcs(context):
    """Reset all functions to standard"""
    clear_list(context[FUNCTIONS], STD_F)

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
    raise NotImplementedError()

def build(doc, delete=False):
    """Compiles specified C file and returns the executable path"""
    raise NotImplementedError()

def run(out):
    """Runs specified executable"""
    raise NotImplementedError()

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
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        pass

#! /usr/bin/env python3
"""interactive c"""
import sys
import os
import subprocess
import tempfile
from shutil import copyfile
import shlex

WELCOME_STR = "Welcome! Type '{}' for help."
GOODBY_STR = "Goodbye!"
CMD_ERR = "Invalid command '{}', see {} for more info"

STD_H = ('<stdio.h>', '<stdlib.h>')
STD_F = (["int main(int argc, char **argv)", 'return 0;'],)

ALIVE = 1
CMDS = 2
USER_INPUT = 3
USER_COMMAND = 4
USER_ARGUMENT = 5
HEADERS = 6
MACROS = 7
GLOBALS = 8
FUNCTIONS = 9

PROMPT_STD = '>> '
PROMPT_ASK = '?> '
PROMPT_MOD = '*> '

C_SKEL = "{}\n{}\n{}\n{}\n{}\n"

def main(argv):
    """main"""
    context = {ALIVE: True,
               CMDS: {'?'   : help_dialog,
                      'help': help_dialog,
                      'exit': exit_program,
                      'quit': exit_program,

                      'addh': add_header,
                      'rmh' : rm_header,
                      'modh': mod_header,
                      'clh' : clear_headers,
                      'llh' : list_headers,

                      'defm': add_macro,
                      'rmm' : rm_macro,
                      'modm': mod_macro,
                      'clm' : clear_macros,
                      'llm' : list_macros,

                      'addg': add_global,
                      'rmg' : rm_global,
                      'modg': mod_global,
                      'clg' : clear_globals,
                      'llg' : list_globals,

                      'deff': add_func,
                      'rmf' : rm_func,
                      'clf' : clear_funcs,
                      'llf' : list_funcs,

                      'prev': preview,
                      'exp' : export,
                      'chk' : check,
                      'exec': execute,},
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
            context[USER_INPUT] = input(PROMPT_STD).strip()
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
            # cmd_func(context)
    # Greet
    print(GOODBY_STR)

def help_dialog(context):
    """Print information about commands"""
    doc = ''
    print("Usage: command argument\nCommand\t\tDescription\n" + 100*'-')
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

def rm_form_with_prompt(the_list, item_is_list=False, item_index=0):
    """Remove user-chosen item from list"""
    pos = choose_between(the_list, item_is_list, item_index)
    if pos == -1:
        print("Invalid selection")
        return
    the_list.pop(pos)

def mod_in_with_prompt(the_list):
    """Modify user-chosen item from list"""
    pos = choose_between(the_list)
    new = ''
    if pos == -1:
        print("Invalid selection")
        return
    new = input(PROMPT_MOD)
    the_list[pos] = new

def clear_list(the_list, standard=None):
    """Clears list in context[index]. If standard is not None, reinits the list
    to it"""
    the_list.clear()
    if standard:
        for std in standard:
            the_list.append(std)

def choose_between(the_list, is_list=False, item_index=0):
    """Print a list and let the user choose. Return the index of the chosen item"""
    user_in = None
    for i, val in enumerate(the_list):
        if is_list:
            print(f'{i} {val[item_index]}')
        else:
            print(f'{i} {val}')
    try:
        user_in = int(input(PROMPT_ASK))
    except ValueError:
        return -1
    if (user_in < 0 or user_in >= len(the_list)):
        return -1
    return user_in

### HEADERS
def add_header(context):
    """Add argument to imported headers (<> and "" required)"""
    add_to(context[HEADERS], context[USER_ARGUMENT])

def rm_header(context):
    """Remove specified header"""
    rm_form_with_prompt(context[HEADERS])

def mod_header(context):
    """Modify one of the defined headers"""
    mod_in_with_prompt(context[HEADERS])

def clear_headers(context):
    """Reset all headers to standard"""
    clear_list(context[HEADERS], STD_H)

def list_headers(context):
    """List all added headers"""
    print("Defined headers:")
    for header in context[HEADERS]:
        print(f'\t#include {header}')

### MACROS
def add_macro(context):
    """Define macro matching the argument (multiline not supported)"""
    add_to(context[MACROS], context[USER_ARGUMENT])

def rm_macro(context):
    """Remove specified macro"""
    rm_form_with_prompt(context[MACROS])

def mod_macro(context):
    """Modify one of the defined macros"""
    mod_in_with_prompt(context[MACROS])

def clear_macros(context):
    """Delete all user defined macros"""
    clear_list(context, MACROS)

def list_macros(context):
    """List all added macros"""
    print("Defined macros:")
    for macro in context[MACROS]:
        print(f'\t#define {macro}')

# GLOBALS
def add_global(context):
    """Add argument to globals"""
    add_to(context[GLOBALS], context[USER_ARGUMENT])

def rm_global(context):
    """Remove specified global"""
    rm_form_with_prompt(context[GLOBALS])

def mod_global(context):
    """Modify one of the defined globals"""
    mod_in_with_prompt(context[GLOBALS])

def clear_globals(context):
    """Clear all defined globals"""
    clear_list(context, GLOBALS)

def list_globals(context):
    """List all defined globals"""
    print("Defined globals:")
    for glob in context[GLOBALS]:
        print(f"\t{glob}")

### FUNCTIONS
def mod_with_editor(original):
    """Modify `original` string into an editor buffer and return the result"""
    tmp_name = ''
    new = ''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as wtmp:
        tmp_name = wtmp.name
        wtmp.write(original)
    if os.environ["EDITOR"]:
        subprocess.run([os.environ["EDITOR"], tmp_name], check=True)
    else:
        subprocess.run(['vi', tmp_name], check=True)
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
    if context[USER_ARGUMENT] == 'main':
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

def rm_func(context):
    """Remove specified global"""
    rm_form_with_prompt(context[FUNCTIONS], True, 0)

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

def merge(headers, macros, globs, functions):
    """Builds a C file with the specified components and returns its path"""
    compiled_headers = ''
    compiled_macros = ''
    compiled_globals = ''
    compiled_prototypes = ''
    compiled_functions = ''
    full_file = ''
    file_path = ''
    # add headers
    for element in headers:
        compiled_headers += '#include ' + element + '\n'
    # add macros
    for element in macros:
        compiled_macros += '#define ' + element + '\n'
    # add globals
    for element in globs:
        compiled_globals += element + ';\n'
    # add prots and funcs
    for element in functions:
        compiled_prototypes += element[0] + ';\n'
        compiled_functions += element[0] + '{\n'
        for line in element[1].splitlines():
            compiled_functions += '\t' + line + '\n'
        compiled_functions += '}\n'

    full_file = C_SKEL.format(compiled_headers, compiled_macros, compiled_globals,
                              compiled_prototypes, compiled_functions)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as wtmp:
        file_path = wtmp.name
        wtmp.write(full_file)
    # write file
    return file_path

def build(doc, delete=False):
    """Compiles specified C file and returns the executable path"""
    raise NotImplementedError()

def run(out):
    """Runs specified executable"""
    raise NotImplementedError()

def execute(context):
    """Build and execute resulting file"""
    doc = merge(context[HEADERS], context[MACROS], context[GLOBALS],
                context[FUNCTIONS])
    out = build(doc)
    run(out)
    os.remove(doc)
    os.remove(out)

def check(context):
    """Check resulting program for errors"""
    doc = merge(context[HEADERS], context[MACROS], context[GLOBALS],
                context[FUNCTIONS])
    build(doc, delete=True)
    os.remove(doc)

def preview(context):
    """Show preview of merged file"""
    doc = merge(context[HEADERS], context[MACROS], context[GLOBALS],
                context[FUNCTIONS])
    print("Document:\n" + 100*'-')
    with open(doc) as file:
        for i, line in enumerate(file):
            print(f'{i}  {line}', end='')
    os.remove(doc)

def export(context):
    """Export file to file with path equals to argument"""
    doc = merge(context[HEADERS], context[MACROS], context[GLOBALS],
                context[FUNCTIONS])
    try:
        copyfile(doc, context[USER_ARGUMENT])
    except IOError as err:
        print("Error during export:", str(err))
    os.remove(doc)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        pass

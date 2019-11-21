#! /usr/bin/env python3
"""interactive c"""
from sys import argv
from shutil import copyfile
import getopt, os, subprocess, tempfile
import shlex

VERSION = '1.0.0'

CMD_ERR_STR = "Invalid command '{}', see {} for more info"

SHORT_OPTS = 'hv'
LONG_OPTS = ('help', 'version')

HELP_MSG = '''Usage: {} [OPTION]
Write a small C program using a quick and easy command prompt.

Options:
\t-h, --help      Display this message
\t-v, --version   Display info on program version

Command prompt:
\tFor help on commands, enter '?' in the command prompt.'''
VERS_MSG = '''{} - BreadyX's Utils (BXU). Version {}
Written by BreadyX, contacts (for bug reports and other):
    GitHub repo (BXU):  https://github.com/BreadyX/bxu'''

STD_H = ('<stdio.h>', '<stdlib.h>')
STD_F = (["int main(int argc, char **argv)", 'return 0;'],)

CMD_OK = 0
CMD_ERR = 1
CMD_EXIT = -1

# ALIVE = 1
# CMDS = 2
# USER_INPUT = 3
# USER_COMMAND = 4
USER_ARGUMENT = 5
HEADERS = 6
MACROS = 7
GLOBALS = 8
FUNCTIONS = 9

PROMPT_STD = '>> '
PROMPT_ASK = '?> '
PROMPT_MOD = '*> '

C_SKEL = "{}\n{}\n{}\n{}\n{}\n"

CMDS = {}  # Declared before main after all function declarations

### UTILITY
def draw_prompt(prompt):
    """Draw prompt"""
    try:
        return input(prompt).strip()
    except EOFError:
        print()  # Maintain good alignment
        return None

def add_to(the_list, arg):
    """Add to index in context"""
    if arg not in the_list:
        the_list.append(arg)
    else:
        print("Item already present")

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
    new = draw_prompt(PROMPT_MOD)
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
    print("Choose:")
    for i, val in enumerate(the_list):
        if is_list:
            print(f'{i}. {val[item_index]}')
        else:
            print(f'{i}. {val}')
    try:
        user_in = int(draw_prompt(PROMPT_ASK))
    except ValueError:
        return -1
    if (user_in < 0 or user_in >= len(the_list)):
        return -1
    return user_in

### MISC
def cmd_help(_):
    """Print information about commands"""
    doc = ''
    out = "Usage: command argument\nCommands:\n"
    for cmd in CMDS:
        doc = 'N.A.' if not CMDS[cmd].__doc__ else CMDS[cmd].__doc__
        out += f'\t{cmd}\t\t{doc}\n'
    print(out)

def cmd_exit(_):
    """Quits program"""
    raise SystemExit()

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
    try:
        if os.environ["EDITOR"]:
            subprocess.run([os.environ["EDITOR"], tmp_name], check=True)
        else:
            subprocess.run(['vi', tmp_name], check=True)
        with open(tmp_name, 'r') as rtmp:
            new = rtmp.read()
    except subprocess.CalledProcessError as error:
        print(f'Error during call to editor: {str(error)}')
        new = original
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
        if element[0] != STD_F[0][0]:
            compiled_prototypes += element[0] + ';\n'
        compiled_functions += element[0] + '{\n'
        for line in element[1].splitlines():
            compiled_functions += '\t' + line + '\n'
        compiled_functions += '}\n'

    full_file = C_SKEL.format(compiled_headers, compiled_macros, compiled_globals,
                              compiled_prototypes, compiled_functions)
    # write file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as wtmp:
        file_path = wtmp.name
        wtmp.write(full_file)
    return file_path

def build(doc, delete=False):
    """Compiles specified C file and returns the executable path"""
    _, compiled = tempfile.mkstemp()
    try:
        subprocess.run(['gcc', '-Wall', '-x', 'c', doc, '-o', compiled], check=True)
    except subprocess.CalledProcessError as error:
        print(f'Error in call to compiler: {str(error)}')
        delete = True
    if delete:
        os.remove(compiled)
        compiled = ''
    return compiled

def execute(context):
    """Build and execute resulting file passing argument"""
    doc = merge(context[HEADERS], context[MACROS], context[GLOBALS],
                context[FUNCTIONS])
    try:
        out = build(doc)
        subprocess.run((out,) + shlex.split(context[USER_ARGUMENT]), check=True)
    except subprocess.CalledProcessError as error:
        print(f'Error has occurred: {str(error)}')
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

### CMDS
CMDS = {'?'   : cmd_help,
        'exit': cmd_exit,

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
        'exec': execute,}

### MAIN
def main(args):
    """main"""
    context = {USER_ARGUMENT: '',
               HEADERS: [],
               MACROS: [],
               GLOBALS: [],
               FUNCTIONS: [],}
    alive = True
    user_input = ''
    split_user_input = ''

    # INIT
    clear_list(context[HEADERS], STD_H)
    clear_list(context[FUNCTIONS], STD_F)
    # Parse argv
    try:
        opts, _ = getopt.getopt(args[1:], SHORT_OPTS, LONG_OPTS)
        for opt, _ in opts:
            if opt in ('-h', '--help'):
                print(HELP_MSG.format(os.path.basename(args[0])))
                return  # Program exit if --help
            if opt in ('-v', '--version'):
                print(VERS_MSG.format(os.path.basename(args[0]), VERSION))
                return  # Program exit if --version
            else:
                print(f'Invalid option {opt}')
    except getopt.GetoptError as err:
        print(str(err))
        return  # Program exit if generic GetoptError

    # Loop, prompt, exec
    while alive:
        user_input = draw_prompt(PROMPT_STD)
        if user_input:
            split_user_input = shlex.split(user_input)
            cmd_func = CMDS.get(split_user_input[0], None)
            context[USER_ARGUMENT] = ' '.join(split_user_input[1:])
            try:
                cmd_func(context)
            except TypeError:
                print(CMD_ERR_STR.format(split_user_input[0], '?'))
        elif user_input is None:
            alive = False

if __name__ == '__main__':
    try:
        main(argv)
    except KeyboardInterrupt:
        pass

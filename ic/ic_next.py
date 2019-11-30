#! /usr/bin/env python3
"""interactive c"""
from sys import argv
from shutil import copyfile
import getopt, os, subprocess, tempfile
import shlex

VERSION = '1.0.0'

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

### CMD argument
NO_ARG = 0
OPT_ARG = 1
ARG = 2

### Error messages
CMD_ERR_STR = "Invalid command '{}', see {} for more info"
CMD_INV_ARG = "Invalid argument {}"
CMD_INV_IND = "Invalid index"
CMD_NO_ARG = "No argument given"

### Context access
USER_ARGUMENT = 5
HEADERS = 6
MACROS = 7
GLOBALS = 8
FUNCTIONS = 9

PROMPT_STD = '>> '
PROMPT_ASK = '?> '
PROMPT_MOD = '*> '

C_SKEL = "{}\n{}\n{}\n{}\n{}\n"

CMDS = {}  # Initialized before main after all function declarations

### UTILITY
def get_user_input(prompt=PROMPT_STD):
    """Draw prompt"""
    try:
        return input(prompt).strip()
    except EOFError:
        print()  # Maintain good alignment
        return None

def add_to(the_list, arg):
    """Add to index in context"""
    print("Using dprecated add_to")
    if arg not in the_list:
        the_list.append(arg)

def rm_from_with_prompt(the_list, item_is_list=False, item_index=0):
    """Remove user-chosen item from list"""
    pos = choose_between(the_list, item_is_list, item_index)
    if pos == -1:
        print(CMD_INV_IND)
        return
    the_list.pop(pos)

def mod_in_with_prompt(the_list):
    """Modify user-chosen item from list"""
    pos = choose_between(the_list)
    new = ''
    if pos == -1:
        print(CMD_INV_IND)
        return
    new = get_user_input(PROMPT_MOD)
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
        user_in = int(get_user_input(PROMPT_ASK))
    except ValueError:
        return -1
    if (user_in < 0 or user_in >= len(the_list)):
        return -1
    return user_in

### MISC
def cmd_help(context):
    """Print help str from CMD. If an argument is passed, then print help only
    for that command"""
    if context[USER_ARGUMENT]:
        cmd = context[USER_ARGUMENT]
        try:
            usage = cmd
            if CMDS[cmd][1] == OPT_ARG:
                usage += ' [arg]'
            elif CMDS[cmd][1] == ARG:
                usage += ' arg'
            doc = '...' if not CMDS[cmd][2] else CMDS[cmd][2]
            print('%-12s%s\n%s' % ("Usage", "Description", 100 * '-'))
            print(f'{usage:12}{doc}')
        except KeyError:
            print(CMD_INV_ARG.format(cmd))
    else:
        print("%-12s%s\n%s" % ("Command", "Description", 100 * '-'))
        for cmd in CMDS:
            doc = '...' if not CMDS[cmd][2] else CMDS[cmd][2]
            print(f'{cmd:12}{doc}')

def cmd_exit(_):
    """Wrapper that launches SystemExit"""
    raise SystemExit()

### HEADERS
def add_header(context):
    """Add USER_ARGUMENT to HEADERS list"""
    if context[USER_ARGUMENT]:
        if context[USER_ARGUMENT] not in context[HEADERS]:
            context[HEADERS].append(context[USER_ARGUMENT])
    else:
        print(CMD_NO_ARG)

def rm_header(context):
    """Pop header of specified index (taken from USER_ARGUMENT or
    choose_between()) from HEADERS"""
    chosen = 0
    if not context[USER_ARGUMENT]:
        rm_from_with_prompt(context[HEADERS])
    else:
        try:
            chosen = int(context[USER_ARGUMENT])
            context[HEADERS].pop(chosen)
        except (TypeError, IndexError):
            print(CMD_INV_ARG.format(chosen))

def mod_header(context):
    """Modify header of specified index (taken from USER_ARGUMENT or
    choose_between()) from HEADERS by replacing it with a new input"""
    chosen = 0
    if not context[USER_ARGUMENT]:
        mod_in_with_prompt(context[HEADERS])
    else:
        try:
            chosen = int(context[USER_ARGUMENT])
            context[HEADERS][chosen] = get_user_input(PROMPT_MOD)
        except (TypeError, IndexError):
            print(CMD_INV_ARG.format(chosen))

def clear_headers(context):
    """Reset HEADERS to STD_H"""
    clear_list(context[HEADERS], STD_H)

def list_headers(context):
    """Print contents of HEADERS"""
    out = ''
    for i, header in enumerate(context[HEADERS]):
        out = f'{i}.'
        if header in STD_H:
            out += ' * '
        else:
            out += '   '
        out += f'#include {header}'
        print(out)

### MACROS
def add_macro(context):
    """Add argument to list of defined macros"""
    if context[USER_ARGUMENT]:
        if context[USER_ARGUMENT] not in context[MACROS]:
            context[MACROS].append(context[USER_ARGUMENT])
    else:
        print(CMD_NO_ARG)

def rm_macro(context):
    """Pop macro of specified index (taken from USER_ARGUMENT or
    choose_between()) from MACROS"""
    chosen = 0
    if not context[USER_ARGUMENT]:
        rm_from_with_prompt(context[MACROS])
    else:
        try:
            chosen = int(context[USER_ARGUMENT])
            context[MACROS].pop(chosen)
        except (TypeError, IndexError):
            print(CMD_INV_ARG.format(chosen))

def mod_macro(context):
    """Modify macro of specified index (taken from USER_ARGUMENT or
    choose_between()) from MACROS by replacing it with a new input"""
    chosen = 0
    if not context[USER_ARGUMENT]:
        mod_in_with_prompt(context[MACROS])
    else:
        try:
            chosen = int(context[USER_ARGUMENT])
            context[MACROS][chosen] = get_user_input(PROMPT_MOD)
        except (TypeError, IndexError):
            print(CMD_INV_ARG.format(chosen))

def clear_macros(context):
    """Reset MACROS"""
    clear_list(context, MACROS)

def list_macros(context):
    """Print contents of MACROS"""
    for i, macro in enumerate(context[MACROS]):
        print(f'{i}. #define {macro}')

# GLOBALS
def add_global(context):
    """Add argument to globals"""
    add_to(context[GLOBALS], context[USER_ARGUMENT])

def rm_global(context):
    """Remove specified global"""
    rm_from_with_prompt(context[GLOBALS])

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
    rm_from_with_prompt(context[FUNCTIONS], True, 0)

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
CMDS = {'?'   : (cmd_help, OPT_ARG,
                 "Print this dialog. If argument is given print help only for that"),
        'quit': (cmd_exit, NO_ARG, "Quit program"),

        'addh': (add_header, ARG,
                 "Add argument to the list of headers (#include MUST NOT be included)"),
        'rmh' : (rm_header, OPT_ARG,
                 "Remove header with index argument. If no index is given,"
                 "a prompt will ask for one"),
        'modh': (mod_header, OPT_ARG,
                 "Modify header with index argument. If no index is given,"
                 "a prompt will ask for one"),
        'clh' : (clear_headers, NO_ARG, "Remove all user-added headers"),
        'llh' : (list_headers, NO_ARG,
                 "List all added headers. Headers with '*' are standard"),

        'addm': (add_macro, ARG,
                 "Add argument to the list of macros (#define MUST NOT be included)"),
        'rmm' : (rm_macro, OPT_ARG,
                 "Remove macro with index argument. If no index is given,"
                 "a prompt will ask for one"),
        'modm': (mod_macro, OPT_ARG,
                 "Modify macro with index argument. If no index is given,"
                 "a prompt will ask for one"),
        'clm' : (clear_macros, NO_ARG, "Remove all user-added macros"),
        'llm' : (list_macros, NO_ARG, "List all added macros"),

        'addg': (add_global, ARG, ""),
        'rmg' : (rm_global, OPT_ARG, ""),
        'modg': (mod_global, OPT_ARG, ""),
        'clg' : (clear_globals, NO_ARG, ""),
        'llg' : (list_globals, NO_ARG, ""),

        'def' : (add_func, ARG, ""),
        'rmf' : (rm_func, OPT_ARG, ""),
        'clf' : (clear_funcs, NO_ARG, ""),
        'llf' : (list_funcs, NO_ARG, ""),

        'prev': (preview, NO_ARG, ""),
        'exp' : (export, NO_ARG, ""),
        'chk' : (check, NO_ARG, ""),
        'exec': (execute, NO_ARG, ""),}

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
        user_input = get_user_input(PROMPT_STD)
        if user_input:
            split_user_input = shlex.split(user_input)
            try:
                cmd_func = CMDS.get(split_user_input[0], None)[0]
            except TypeError:
                print(CMD_ERR_STR.format(split_user_input[0], '?'))
                continue
            context[USER_ARGUMENT] = ' '.join(split_user_input[1:])
            cmd_func(context)
        elif user_input is None:
            alive = False

if __name__ == '__main__':
    try:
        main(argv)
    except KeyboardInterrupt:
        print()  # good alignment

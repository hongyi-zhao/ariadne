import os 
from percol.finder import FinderMultiQueryRegex
myhost = os.uname()[1] # get hostname for left prompt
myhost = myhost.strip()


#https://github.com/hongyi-zhao/recent2/blob/5b072ff5d6419c444bb013b88e5e2a4de19b0851/recent2.py#L24
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
LIGHTCYAN = '\033[1;36m'
LIGHTGRAY = '\033[0;37m'
YELLOW = '\033[0;33m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# -*- coding: utf-8 -*-
# variables for keybindings to use both in prompt strings and setting the keymap
push_stack = "C-p"			# add command to bottom of stack 
pop_stack = "M-p"			# remove bottom command from stack
save_stack = "M-s"			# save commands in stack as rerun.sh

filter_dups = "C-q"			# filter out duplicate commands
filter_exit0 = "C-e"		# toggle display of non-zero exit status (or old commands from before this feature, retroactively set to-999)

filter_bydir = "C-d"		# fliter by current path
return_dir = "M-d"			# return path and exit
return_both = "M-b"         # return path and command separated by ;

toggle_host = "C-h"
next_host = "C-n"
switch_finder = "C-f"		# toggle regex finder

hide_field_1 = "<f1>"		# toggle show date column
hide_field_2 = "<f2>"		# toggle show path column
hide_field_3 = "<f3>"		# toggle show command column


## Reformat keybindings for prompt display
def pretty_key(key): 
    tmp = key.replace('C-','C-')
    tmp = tmp.replace('M-', 'M-')
    tmp = tmp.replace('<', '')
    tmp = tmp.replace('>', '')

    tmp = tmp.replace('f1', 'F1')
    tmp = tmp.replace('f2', 'F2')
    tmp = tmp.replace('f3', 'F3')
    return tmp

## Field seperator, originally used ' <> ', which works well visually but uses a lot of space
#https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols
# ▌ 	 258C 	 left half block
# ▐ 	 2590 	 right half block 
FIELD_SEP = '▐▌' 
# field seperator colours for exit code == 0 and != 0
percol.view.exit0_color = 'blue'
percol.view.exitnot0_color = 'red'

## Left and right prompt format, works best on a wide screen and black bg
# see https://github.com/mooz/percol for more formatting options
percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("reverse", "on_black", "white")
percol.view.CANDIDATES_LINE_MARKED   = ("dim", "on_black", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.STACKLINE = 'Fold:F1,F2,F3 Push:C-p Pop:M-p Script:M-s Dir:M-d Dircmd:M-b'
#https://groups.google.com/g/comp.lang.python/c/tmX_j19qk2I/m/EBxHycZYCAAJ
#percol.view.STACKLINE = percol.view.STACKLINE.replace('D', Term.UNDERLINE + 'D' + Term.ENDC)
percol.view.FOLDED = '' # need to find the right mono-font for mac? Seems to work with "input mono narrow", otherwise use '..'

percol.view.PROMPT = f'<bold><cyan>%H ({pretty_key(toggle_host)}/{pretty_key(next_host)})</cyan></bold>> %q'
percol.view.prompt_replacees["F"] = lambda self, **args: self.model.finder.get_name() # insert finder
percol.view.prompt_replacees["H"] = lambda self, **args: self.model.finder.host # insert host name or 'all hosts'

# percol.view.RPROMPT = f"{pretty_key(switch_finder)}:%F \
# Dir:{pretty_key(return_dir)} \
# Cwd:{pretty_key(filter_bydir)} \
# Uniq:{pretty_key(filter_dups)} \
# Ecode:{pretty_key(filter_exit0)} \
# Fold:{pretty_key(hide_field_1)},\
# {pretty_key(hide_field_2)},\
# {pretty_key(hide_field_3)}\
# "

# Togle green and bold when filtering for exit == 0 and duplicate commands
# ugh, nested if...else. Isn't there a better way?

percol.view.__class__.RPROMPT = property(
    lambda self:
    f"{pretty_key(switch_finder)}:%F \
Cwd:{pretty_key(filter_bydir)} \
<green><bold>Uniq:{pretty_key(filter_dups)}</green></bold> \
<green><bold>Ecode:{pretty_key(filter_exit0)}</green></bold>" if percol.model.finder.recent_commands and percol.model.finder.exit0 \
    else (
f"{pretty_key(switch_finder)}:%F \
Cwd:{pretty_key(filter_bydir)} \
<green><bold>Uniq:{pretty_key(filter_dups)}</green></bold> \
Ecode:{pretty_key(filter_exit0)}" if percol.model.finder.recent_commands \
    else (
f"{pretty_key(switch_finder)}:%F \
Cwd:{pretty_key(filter_bydir)} \
Uniq:{pretty_key(filter_dups)} \
<green><bold>Ecode:{pretty_key(filter_exit0)}</bold></green>" if percol.model.finder.exit0
        else 
f"{pretty_key(switch_finder)}:%F \
Cwd:{pretty_key(filter_bydir)} \
Uniq:{pretty_key(filter_dups)} \
Ecode:{pretty_key(filter_exit0)}")))

## Set keybindings
percol.import_keymap({
    # "C-i"         : lambda percol: percol.switch_model(), # not sure what this is, invert? Doesn't work here
    # text
    "C-h"         : lambda percol: percol.command.delete_backward_char(),
    "<backspace>" : lambda percol: percol.command.delete_backward_char(),
    "C-w"         : lambda percol: percol.command.delete_backward_word(),
    "C-u"         : lambda percol: percol.command.clear_query(),
    "<dc>"        : lambda percol: percol.command.delete_forward_char(),
    # caret
    "<left>"      : lambda percol: percol.command.backward_char(),
    "<right>"     : lambda percol: percol.command.forward_char(),
    # line
    "<down>"      : lambda percol: percol.command.select_next(),
    "<up>"        : lambda percol: percol.command.select_previous(),
    # page
    "<npage>"     : lambda percol: percol.command.select_next_page(),
    "<ppage>"     : lambda percol: percol.command.select_previous_page(),
    # top / bottom
    "<home>"      : lambda percol: percol.command.select_top(),
    "<end>"       : lambda percol: percol.command.select_bottom(),
    # mark
    # finish
    "RET"         : lambda percol: percol.finish(), # Is RET never sent? #seems not, doesn't respond to finish_f either -gw
    "C-m"         : lambda percol: percol.finish(), # for some reason can't assign to anything else, breaks RET binding
    # "C-j"         : lambda percol: percol.finish(),
    # "C-c"         : lambda percol: percol.cancel(),
    "C-n" : lambda percol: percol.command.select_next(),

    # select multiple lines. Will return list of commands or paths, probably of limited usefulness?
    "C-o"       : lambda percol: percol.command.toggle_mark_and_next(),

    hide_field_1 : lambda percol: percol.command.toggle_date(),                       # Fold date field
    hide_field_2 : lambda percol: percol.command.toggle_execdir(),                    # Fold directory field
    hide_field_3 : lambda percol: percol.command.toggle_command(),                    # Fold command field
    filter_bydir : lambda percol: percol.command.cwd_filter(),                        # Add current path to queries
    return_dir   : lambda percol: percol.finish(field=1),                             # Return directory
    return_both  : lambda percol: percol.finish(field=-1),                            # Return 'dir; command'
    toggle_host  : lambda percol: percol.command.toggle_host(),                       # Filter by local host or all hosts
    next_host    : lambda percol: percol.command.next_host(),                         # Filter by next host in known hosts list
    filter_dups  : lambda percol: percol.command.toggle_recent(),                     # Togggle filtering of duplicates
    filter_exit0 : lambda percol: percol.command.toggle_exit0(),                      # Toggle filtering by exit status
    push_stack   : lambda percol: percol.command.fill_stack(),                        # Add to stack
    pop_stack    : lambda percol: percol.command.pop_stack(),                         # Remove from stack
    save_stack   : lambda percol: percol.finish_and_save(),                           # save stack as 'rerun.sh'
    switch_finder: lambda percol: percol.command.toggle_finder(FinderMultiQueryRegex) # switch between normal and regex finders
})    

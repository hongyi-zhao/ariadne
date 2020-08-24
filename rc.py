import os 
from percol.finder import FinderMultiQueryRegex
myhost = os.uname()[1] # get hostname for left prompt
myhost = myhost.strip()

# -*- coding: utf-8 -*-
# variables for keybindings to use both in prompt strings and setting the keymap
push_stack = "C-p"			# add command to bottom of stack 
pop_stack = "M-p"			# remove bottom command from stack
save_stack = "C-s"			# save commands in stack as rerun.sh
filter_dups = "M-r"			# filter out duplicate commands
filter_exit0 = "M-t"		# toggle display of non-zero exit status (or old commands from before this feature, retroactively set to-999)
return_dir = "C-d"			# return path and exit
return_both = "C-b"         # return path and command separated by ;
toggle_host = "M-h"
next_host = "M-n"
filter_bydir = "C-l"		# fliter by current path
hide_field_1 = "<f1>"		# toggle show date column
hide_field_2 = "<f2>"		# toggle show path column
hide_field_3 = "<f3>"		# toggle show command column
switch_finder = "M-m"		# toggle regex finder

def pretty_key(key): # modify for cleaner display in the console prompts
    tmp = key.replace('C-','^')
    # tmp = key.replace('C-','⎈') # the official unicode symbol? doesn't work well for me
    tmp = tmp.replace('M-', u'⎇ ')# this may not work on all terminals, comment out if needed
    tmp = tmp.replace('<', '')
    tmp = tmp.replace('>', '')

    tmp = tmp.replace('f1', 'F1')
    tmp = tmp.replace('f2', 'F2')
    tmp = tmp.replace('f3', 'F3')
    return tmp

# works well enough on black background
# see https://github.com/mooz/percol for more formatting options

# originally used ' <> ', which works well visually but uses a lot of space
FIELD_SEP = '║' # set for cli.py

percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("reverse", "on_black", "white")
percol.view.CANDIDATES_LINE_MARKED   = ("dim", "on_black", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.STACKLINE = 'v════v Script ══ Add:%s ══ Remove:%s ══ Save "rerun.sh":%s v════v'\
	%(pretty_key(push_stack),
        pretty_key(pop_stack),
        pretty_key(save_stack))
percol.view.FOLDED = '…' # need to find the right mono-font for mac? Seems to work with "input mono narrow", otherwise use '..'

def bold(is_set,text):
    if is_set:
        return f'<bold>{text}</bold>'
    else:
        return f'{text}'


# Set left and right prompt, assumes a wide screen
percol.view.PROMPT = f'<bold><cyan>%H ({pretty_key(toggle_host)}/{pretty_key(next_host)})</cyan></bold>> %q'
percol.view.prompt_replacees["F"] = lambda self, **args: self.model.finder.get_name()
percol.view.prompt_replacees["H"] = lambda self, **args: self.model.finder.host

# percol.view.RPROMPT = f"{pretty_key(switch_finder)}:%F \
# Path:{pretty_key(return_dir)} \
# Local:{pretty_key(filter_bydir)} \
# Unique:{pretty_key(filter_dups)} \
# Exit0:{pretty_key(filter_exit0)} \
# Fold:{pretty_key(hide_field_1)},\
# {pretty_key(hide_field_2)},\
# {pretty_key(hide_field_3)}\
# "

# Togle green and bold when filtering for exit == 0 and duplicate commands
# ugh, nested if...else. Isn't there a better way?
percol.view.__class__.RPROMPT = property(
    lambda self: 
    f"{pretty_key(switch_finder)}:%F \
Path:{pretty_key(return_dir)} \
Local:{pretty_key(filter_bydir)} \
<green><bold>Unique:{pretty_key(filter_dups)}</green></bold> \
<green><bold>Exit0:{pretty_key(filter_exit0)}</green></bold> \
Fold:{pretty_key(hide_field_1)},\
{pretty_key(hide_field_2)},\
{pretty_key(hide_field_3)}" if percol.model.finder.recent_commands and percol.model.finder.exit0 \
    else (
f"{pretty_key(switch_finder)}:%F \
Path:{pretty_key(return_dir)} \
Local:{pretty_key(filter_bydir)} \
<green><bold>Unique:{pretty_key(filter_dups)}</green></bold> \
Exit0:{pretty_key(filter_exit0)} \
Fold:{pretty_key(hide_field_1)},\
{pretty_key(hide_field_2)},\
{pretty_key(hide_field_3)}" if percol.model.finder.recent_commands \
    else (
f"{pretty_key(switch_finder)}:%F \
Path:{pretty_key(return_dir)} \
Local:{pretty_key(filter_bydir)} \
Unique:{pretty_key(filter_dups)} \
<green><bold>Exit0:{pretty_key(filter_exit0)}</bold></green> \
Fold:{pretty_key(hide_field_1)},\
{pretty_key(hide_field_2)},\
{pretty_key(hide_field_3)}" if percol.model.finder.exit0
        else 
f"{pretty_key(switch_finder)}:%F \
Path:{pretty_key(return_dir)} \
Local:{pretty_key(filter_bydir)} \
Unique:{pretty_key(filter_dups)} \
Exit0:{pretty_key(filter_exit0)} \
Fold:{pretty_key(hide_field_1)},\
{pretty_key(hide_field_2)},\
{pretty_key(hide_field_3)}")))


# percol.view.prompt_replacees["x"] = lambda self, **args: bold(self.model.finder.exit0,'EXIT')

# percol.view.__class__.RPROMPT = property(
#     lambda self: \
#     u"<bold><blue>QUERY </blue>[a]:</bold> %q" if percol.model.finder.case_insensitive \
#     else u"<bold><green>QUERY </green>[A]:</bold> %q"
# )

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

    hide_field_1 : lambda percol: percol.command.toggle_date(),
    hide_field_2 : lambda percol: percol.command.toggle_execdir(),
    hide_field_3 : lambda percol: percol.command.toggle_command(),
    filter_bydir : lambda percol: percol.command.cwd_filter(),
    return_dir   : lambda percol: percol.finish(field=1),
    return_both  : lambda percol: percol.finish(field=-1),
    toggle_host  : lambda percol: percol.command.toggle_host(),
    next_host    : lambda percol: percol.command.next_host(),
    filter_dups  : lambda percol: percol.command.toggle_recent(),
    filter_exit0 : lambda percol: percol.command.toggle_exit0(),
    push_stack   : lambda percol: percol.command.fill_stack(),
    pop_stack    : lambda percol: percol.command.pop_stack(),
    save_stack   : lambda percol: percol.finish_and_save(),
    switch_finder: lambda percol: percol.command.toggle_finder(FinderMultiQueryRegex) # switch between normal and regex finders
})    

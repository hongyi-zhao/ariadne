import os 
from percol.finder import FinderMultiQueryRegex
myhost = os.uname()[1] # get hostname for left prompt

# -*- coding: utf-8 -*-
# variables for keybindings to use both in prompt strings and setting the keymap
push_stack = "C-s"			# add command to bottom of stack 
pop_stack = "M-s"			# remove bottom command from stack
save_stack = "C-t"			# save commands in stack as rerun.sh
filter_dups = "M-r"			# filter out duplicate commands
filter_exit0 = "M-t"		# toggle display of non-zero exit status (or old commands from before this feature, retroactively set to-999)
return_dir = "C-d"			# return path and exit
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
    return tmp

# works well enough on black background
# see https://github.com/mooz/percol for more formatting options
FIELD_SEP = '║' # originally used ' <> ', which works well visually but uses a lot of space
percol.view.__class__.FIELD_SEP = property(lambda self: FIELD_SEP)
percol.command.set_field_sep(FIELD_SEP)

percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("reverse", "on_black", "white")
percol.view.CANDIDATES_LINE_MARKED   = ("dim", "on_black", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.STACKLINE = 'v════v Command Stack ══ push:%s ══ pop:%s ══ save as "rerun.sh":%s v════v'\
	%(pretty_key(push_stack),
        pretty_key(pop_stack),
        pretty_key(save_stack))
percol.view.FOLDED = '…' # need to find the right mono-font for mac? Seems to work with "input mono narrow", otherwise use '..'

# Set left and right prompt, assumes a wide screen
percol.view.PROMPT = f'<bold><cyan>{myhost}</cyan></bold>> %q'
percol.view.prompt_replacees["F"] = lambda self, **args: self.model.finder.get_name()
percol.view.RPROMPT = f"Finder({pretty_key(switch_finder)}):%F \
Path:{pretty_key(return_dir)} \
Local:{pretty_key(filter_bydir)} \
Unique:{pretty_key(filter_dups)} \
Exit0:{pretty_key(filter_exit0)} \
Show/Hide{pretty_key(hide_field_1)},\
{pretty_key(hide_field_2)},\
{pretty_key(hide_field_3)}\
"

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
    return_dir : lambda percol: percol.finish(field=1),
    "C-r" : lambda percol: percol.finish(field=2),
    "C-b" : lambda percol: percol.finish(field=-1),
    filter_dups : lambda percol: percol.command.toggle_recent(),
    filter_exit0 : lambda percol: percol.command.toggle_exit0(),
    push_stack : lambda percol: percol.command.fill_stack(),
    pop_stack : lambda percol: percol.command.pop_stack(),
    save_stack : lambda percol: percol.finish_and_save(),
    switch_finder: lambda percol: percol.command.toggle_finder(FinderMultiQueryRegex) # switch between normal and regex finders
})    

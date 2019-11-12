# -*- coding: utf-8 -*-
push_stack = "C-s"
pop_stack = "M-s"
save_stack = "C-t"
filter_dups = "M-r"
filter_exit0 = "M-t"
return_dir = "C-d"
filter_bydir = "C-l"
hide_field_1 = "<f1>"
hide_field_2 = "<f2>"
hide_field_3 = "<f3>"

def pretty_key(key): # modify for cleaner display in the console
    tmp = key.replace('C-','^')
    # tmp = tmp.replace('M-', u'⎇ ')# need to find a better alternative for mono fonts
    tmp = tmp.replace('<', '')
    tmp = tmp.replace('>', '')
    return tmp

FIELD_SEP = '║' 
percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("underline", "on_blue", "white","bold")
percol.view.CANDIDATES_LINE_MARKED   = ("bold", "on_cyan", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.STACKLINE = 'v════v Command Stack ══ push:%s ══ pop:%s ══ save as "rerun.sh":%s v════v'\
	%(pretty_key(push_stack),
        pretty_key(pop_stack),
        pretty_key(save_stack))
percol.view.FOLDED = '…' # need to find the right mono-font for mac? Seems to work with "input mono narrow"
percol.view.RPROMPT = 'Path:%s Local:%s Unique:%s Exit0:%s Show/Hide:%s,%s,%s'\
    %(  pretty_key(return_dir),
        pretty_key(filter_bydir),
        pretty_key(filter_dups),
        pretty_key(filter_exit0),
        pretty_key(hide_field_1),
        pretty_key(hide_field_2),
        pretty_key(hide_field_3))

percol.import_keymap({
    "C-i"         : lambda percol: percol.switch_model(),
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
    "C-SPC"       : lambda percol: percol.command.toggle_mark_and_next(),
    # finish
    "RET"         : lambda percol: percol.finish(), # Is RET never sent? #seems not, doesn't respond to finish_f either - gaw
    "C-m"         : lambda percol: percol.finish(),
    # "C-j"         : lambda percol: percol.finish(),
    # "C-c"         : lambda percol: percol.cancel(),

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
})    

percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("underline", "on_blue", "white","bold")
percol.view.CANDIDATES_LINE_MARKED   = ("bold", "on_cyan", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.FIELD_SEP = ' >< ' #other possiblities: ' ◆ ', ' 🞛  ' etc
# 
percol.view.FOLDED = '..' # not sure how to get '…' working for mac

percol.command.set_field_sep(percol.view.FIELD_SEP)

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

    "<f1>" : lambda percol: percol.command.toggle_date(),
    "<f2>" : lambda percol: percol.command.toggle_execdir(),
    "<f3>" : lambda percol: percol.command.toggle_command(),
    "C-l" : lambda percol: percol.command.cwd_filter(),
    "C-d" : lambda percol: percol.finish(field=1),
    "C-r" : lambda percol: percol.finish(field=2),
    "M-r" : lambda percol: percol.command.toggle_recent(),
    "C-s" : lambda percol: percol.command.fill_stack(),
    "M-s" : lambda percol: percol.command.pop_stack(),
    "C-t" : lambda percol: percol.finish_and_save(),
})    

- [Installation](#installation)
  - [Zsh](#zsh)
  - [Bash](#bash)
  - [Fish](#fish)
- [Key bindings](#keybindigs)
- [Configuration](#configuration)

# ariadne

Ariadne enables comprehensive CLI shell history logging, combined with interactive searching, using a modified version of Masafumi Oyamada's interactive grep tool: percol (https://github.com/mooz/percol). The CLI logging in `bash/zsh` is modified from the following scripts:

- http://stackoverflow.com/questions/945288/saving-current-directory-to-bash-history
- https://gist.github.com/jeetsukumaran/2202879)

If you derive little joy from memorizing the arbitrary incantations and arcana of the unix command line this might be for you. With this you can:

1. Reverse search through previous commands and the paths where they were run
2. Extract either the path or command
3. Filter by current path
4. Filter out duplicate commands
5. Filter by exit status 0
6. Hide/show date, command, path fields in search output
7. Stack commands and save to a script (rerun.sh)
8. Filter by host etc

`Ctrl+R` is captured to replace the default history search to pipe the log file (`~/.<zsh/fish/bash>_log`) through the modified percol fuzzy finder. The log file records time, date, directory, host, exit status and command of every command entered. This makes it easy to retrieve commands in a new project directory based on a similar older project, find a deeply nested project dir by the command etc. I find I need this often when running scientific software in the unix world. Similarly `Ctrl+Alt+R` is mapped to read a master log file, which can be used to record commands on multiple hosts if sym-linked to a file in a cloud sync directory. 

![Current look](https://github.com/gawells/demos/blob/master/screen02.png)
Current (more compact) look. Blue indicates exit status = 0, red ≠ 0.
 
![Animation of old look](https://github.com/gawells/demos/blob/master/ariadne1.gif)
Animation of old look-and-feel.

## Installation
    $ git clone https://github.com/gawells/ariadne
    $ cd ariadne
    
### Zsh

    $ ./setup.py -z

Add the following to `~/.zshrc` 

    source ~/.config/zsh/ariadne/ariadne.zsh
    
### Bash
# First, download and source the following package in ~/.bashrc:
# https://github.com/rcaloras/bash-preexec
#
# Then add something like the following to ~/.bashrc:
  export ariadne_bash_log=$HOME/.history/ariadne-bash-log
# If you also want to save the history to master log:   
#  #export ariadne_bash_master_log=$HOME/.history/ariadne-bash-master-log
 source $script_realdirname/ariadne.sh
    
### Fish
    
    $ ./setup.py -f
    
Add the contents of `./config.fish` to `~/.config/fish/config.fish`

## Key bindings

- Ctrl+R          : Invoke command history search
- Ctrl+Alt+R      : Invoke command history search on master file 

In ariadne:

- F1,F2,F3        : Hide/show date, execution path and command, respectively
- Enter,Ctrl+m    : Extract command(s)
- Ctrl+d          : Extract path(s)
- Ctrl+b          : Extract path and command, seperated by ';'
- Ctrl+l          : Filter by current directory
- Alt+r           : Toggle filter for duplicate commands
- Alt+t           : Toggle filter commands with exit staus 0
- Ctrl+SPC        : Select entry (useful for extracting salient commands for future recipes?)
- Ctrl+s          : Push command to stack
- Alt+s           : Pop command from stack
- Ctrl+t          : Save stack (as 'rerun'sh') and exit
- Alt-m           : Switch between normal and regex search 
- Alt-h           : Switch between all hosts and current host (mostly for master file)
- Alt-n           : Cycle through hosts (mostly for master file)

## Configuration

Configuration is specified in `rc.py`, currently under `$HOME/.config/<bash/zsh>/ariadne/`

Default config:
```python
import os 
from percol.finder import FinderMultiQueryRegex
myhost = os.uname()[1] # get hostname for left prompt
myhost = myhost.strip()

# -*- coding: utf-8 -*-
# variables for keybindings to use both in prompt strings and setting the keymap
push_stack = "C-p"          # add command to bottom of stack 
pop_stack = "M-p"           # remove bottom command from stack
save_stack = "C-s"          # save commands in stack as rerun.sh
filter_dups = "M-r"         # filter out duplicate commands
filter_exit0 = "M-t"        # toggle display of non-zero exit status (or old commands from before this feature, retroactively set to-999)
return_dir = "C-d"          # return path and exit
return_both = "C-b"         # return path and command separated by ;
toggle_host = "M-h"
next_host = "M-n"
filter_bydir = "C-l"        # fliter by current path
hide_field_1 = "<f1>"       # toggle show date column
hide_field_2 = "<f2>"       # toggle show path column
hide_field_3 = "<f3>"       # toggle show command column
switch_finder = "M-m"       # toggle regex finder

## Reformat keybindings for prompt display
def pretty_key(key): 
    tmp = key.replace('C-','^')
    # tmp = key.replace('C-','⎈') # the official unicode symbol? doesn't work well for me
    tmp = tmp.replace('M-', u'⎇ ') # this may not work on all terminals, comment out if needed
    tmp = tmp.replace('<', '')
    tmp = tmp.replace('>', '')

    tmp = tmp.replace('f1', 'F1')
    tmp = tmp.replace('f2', 'F2')
    tmp = tmp.replace('f3', 'F3')
    return tmp

## Field seperator, originally used ' <> ', which works well visually but uses a lot of space
FIELD_SEP = '║' 
# field seperator colours for exit == 0 and =/= 0
percol.view.exit0_color = 'blue'
percol.view.exitnot0_color = 'red'

## Left and right prompt format, works best on a wide screen and black bg
# see https://github.com/mooz/percol for more formatting options
percol.view.CANDIDATES_LINE_BASIC    = ("on_default", "default")
percol.view.CANDIDATES_LINE_SELECTED = ("reverse", "on_black", "white")
percol.view.CANDIDATES_LINE_MARKED   = ("dim", "on_black", "black")
percol.view.CANDIDATES_LINE_QUERY    = ("green", "bold")
percol.view.STACKLINE = 'v════v Script ══ Add:%s ══ Remove:%s ══ Save "rerun.sh":%s v════v'\
    %(pretty_key(push_stack),
        pretty_key(pop_stack),
        pretty_key(save_stack))
percol.view.FOLDED = '…' # need to find the right mono-font for mac? Seems to work with "input mono narrow", otherwise use '..'

percol.view.PROMPT = f'<bold><cyan>%H ({pretty_key(toggle_host)}/{pretty_key(next_host)})</cyan></bold>> %q'
percol.view.prompt_replacees["F"] = lambda self, **args: self.model.finder.get_name() # insert finder
percol.view.prompt_replacees["H"] = lambda self, **args: self.model.finder.host # insert host name or 'all hosts'

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
```


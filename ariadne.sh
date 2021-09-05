#!/usr/bin/env bash
script_realdirname=$(dirname "$(realpath -e "${BASH_SOURCE[0]}")")


_ariadne() { # was _loghistory :)
# Modified for zsh - Gordon Wells 2014/08

# Detailed history log of shell activities, including time stamps, working directory etc.
# Based on 'hcmnt' by Dennis Williamson - 2009-06-05 - updated 2009-06-19
# (http://stackoverflow.com/questions/945288/saving-current-directory-to-bash-history)
# (https://gist.github.com/jeetsukumaran/2202879)
#
# Set the bash variable PROMPT_COMMAND to the name of this function and include
# these options:
#
#     e - add the output of an extra command contained in the histentrycmdextra variable
#     h - add the hostname
#     y - add the terminal device (tty)
#     u - add the username
#     n - don't add the directory
#     t - add the from and to directories for cd commands
#     l - path to the log file (default = $HOME/.bash_log)
#     ext or a variable
#
## Add something like the following to ~/.bashrc:
# source $script_realdirname/ariadne.sh
# export PROMPT_COMMAND='_ariadne -h -u '
##

    local script=$FUNCNAME
    local histentrycmd=
    local cwd=
    local extra=
    local text=
    #local logfile="$HOME/.bash_log"
    #local masterlog
    local logfile="$ariadne_bash_log"
    #local masterlog="$ariadne_bash_master_log"
    local hostname=
    local histentry=
    local histleader=
    local datetimestamp=
    local histlinenum=
    local username=
    local options=":hyunte:l:m:"
    local option=
    OPTIND=1
    local usage="Usage: $script [-h] [-y] [-u] [-n|-t] [-e] [text] [-l logfile]"

    local ExtraOpt=
    local NoneOpt=
    local ToOpt=
    local tty=
    local ip=

    # *** process options to set flags ***

    while getopts $options option
    do
        case $option in
            h ) hostname=$(hostname);;
            y ) tty=$(tty);;
            u ) username=$USER;;
            n ) if [[ -n $ToOpt ]]
                then
                    echo "$script: can't include both -n and -t."
                    echo $usage
                    return 1
                else
                    NoneOpt=1       # don't include path
                fi;;
            t ) if [[ -n $NoneOpt  ]]
                then
                    echo "$script: can't include both -n and -t."
                    echo $usage
                    return 1
                else
                    ToOpt=1         # cd shows "from -> to"
                fi;;
            e ) ExtraOpt=1;histentrycmdextra=$OPTARG;;        # include histentrycmdextra
            l ) logfile=$OPTARG;;
            m ) masterlog=$OPTARG;;
            : ) echo "$script: missing filename: -$OPTARG."
                echo $usage
                return 1;;
            * ) echo "$script: invalid option: -$OPTARG."
                echo $usage
                return 1;;
        esac
    done

    text=($@)                       # arguments after the options are saved to add to the comment
    text="${text[*]:$OPTIND - 1:${#text[*]}}"

    # add the previous command(s) to the history file immediately
    # so that the history file is in sync across multiple shell sessions
    export HISTTIMEFORMAT="%y-%m-%d %T "
    history -a

    # grab the most recent command from the command history
    histentry=$(history 1)

    # parse it out
    # for some reason need to split it like this, regex inline doesn't work on my mac
    re=' *([0-9]* *[0-9]*-[0-9]*-[0-9]* *[0-9]*:[0-9]*:[0-9]*)'
    [[ $histentry =~ $re ]] && histleader=${BASH_REMATCH}

    re=' *([0-9]*)' 
    [[ $histleader =~ $re ]] && histlinenum=${BASH_REMATCH[1]}

    re='.* ([0-9]*-[0-9]*-[0-9]* *[0-9]*:[0-9]*:[0-9]*)'
    [[ $histleader =~ $re ]] && datetimestamp=${BASH_REMATCH[1]}

    re=' *[0-9]* *[0-9]*-[0-9]*-[0-9]* *[0-9]*:[0-9]*:[0-9]* (.*)'
    [[ $histentry =~ $re ]] && histentrycmd=${BASH_REMATCH[1]}

    # protect against relogging previous command
    # if all that was actually entered by the user
    # was a (no-op) blank line
    # echo "${#__PREV_HISTCMD} ${#__PREV_HISTLINE}"
    if [[ -z "$__PREV_HISTCMD" ]]
    then
        # new shell; initialize variables for next command
    	# echo "$__PREV_HISTCMD $__PREV_HISTLINE"
        export __PREV_HISTLINE=$histlinenum
        export __PREV_HISTCMD=$histentrycmd
        return
    fi
    if [[ $histlinenum == $__PREV_HISTLINE  && $histentrycmd == $__PREV_HISTCMD ]]
    then
        # no new command was actually entered
        return
    else
        # new command entered; store for next comparison
        export __PREV_HISTLINE=$histlinenum
        export __PREV_HISTCMD=$histentrycmd
    fi

    if [[ -z "$NoneOpt" ]]            # are we adding the directory?
    then
        if [[ ${histentrycmd%% *} == "cd" \
         || ${histentrycmd%% *} == "j"  \
         || $histentrycmd%% =~ "^~-" ]]    # if it's a cd command, we want the old directory
         # modified for autjump (j) and named directories (~), not sure how to deal with autocd
         # Doesn't detect failure to change to restricted directories
        then                             #   so the comment matches other commands "where *were* you when this was done?"
            if [[ -z "$OLDPWD" ]]
            then
                OLDPWD="$HOME"
            fi
            if [[ -n $ToOpt ]]
            then
                cwd="$OLDPWD -> $PWD"    # show "from -> to" for cd
            else
                cwd=$OLDPWD              # just show "from"
            fi
        else
            cwd=$PWD                     # it's not a cd, so just show where we are
        fi
    fi

    if [[ -n $ExtraOpt && -n $histentrycmdextra ]]    # do we want a little something extra?
    then
        extra=$(eval ${histentrycmdextra})
    fi

    # build the string (if text or extra aren't empty, add them with some decoration)
    # note on ${var+$var} format: empty if unset but expands to var value if set?
    # '###' chosen because it's unlikely to appear in a typical shell command, also 
    # a bit easier on my eye than '~~~'
    histentrycmd="${histentrycmd} ### ${datetimestamp} , ${histlinenum} , \
    ${username:+$username} , ${hostname:+$hostname} , ${cwd} ,  \
    ${tty:+[$tty] } , ${ip:+[$ip] } , ${extra:+$extra }"
    
    # save the entry in a logfile
    echo "$histentrycmd" >> $logfile || (echo "$script: file error." ; return 1;)

    # save in master log file
    if [[ -n ${masterlog} ]]
    then
        echo "$histentrycmd" >> $masterlog || (echo "$script: file error." ; return 1)
    fi
} 

# modified from https://github.com/mooz/percol#zsh-history-search

function percol_sel_log_history() {
    unset SEP
    RCFILE="$script_realdirname/rc.py"
    PERCOL="$script_realdirname/bin/percol"
    PYTHONPATH="$script_realdirname/percol":$PYTHONPATH
    $PERCOL --reverse --rcfile=$RCFILE $ariadne_bash_log
}

function percol_sel_log_master_history() {
    unset SEP
    RCFILE="$script_realdirname/rc.py"
    PERCOL="$script_realdirname/bin/percol"
    PYTHONPATH="$script_realdirname/percol":$PYTHONPATH
    $PERCOL --reverse --rcfile=$RCFILE $ariadne_bash_master_log
}



#https://zsh.sourceforge.io/Doc/Release/Functions.html#Hook-Functions
#precmd

#    Executed before each prompt. Note that precommand functions are not re-executed simply because the command line is redrawn, as happens, for example, when a notification about an exiting job is displayed.
#preexec

#    Executed just after a command has been read and is about to be executed. If the history mechanism is active (regardless of whether the line was discarded from the history buffer), the string that the user typed is passed as the first argument, otherwise it is an empty string. The actual command that will be executed (including expanded aliases) is passed in two different forms: the second argument is a single-line, size-limited version of the command (with things like function bodies elided); the third argument contains the full text that is being executed.


function ariadne_precmd() {
  #https://bleepcoder.com/bash-git-prompt/259531236/iterm2-shell-integration-breaks-git-prompt-command-fail
  #Replace `$?' with `$__bp_last_ret_value' with the help of bash preexec hooks:
  # https://github.com/rcaloras/bash-preexec
  ar_result=$__bp_last_ret_value
  #_ariadne -h -u -e "echo -n $ar_result" -m "$ariadne_bash_master_log"
  _ariadne -h -u -e "echo -n $ar_result"
}


#https://superuser.com/questions/892658/remote-ssh-commands-bash-bind-warning-line-editing-not-enabled/892682
#https://groups.google.com/g/comp.unix.shell/c/UfAkvZ1C10I/m/gPxb5sJUBwAJ
if set -o | egrep '\bon$' | egrep -q '^(vi|emacs)\b'; then
  # https://github.com/dvorka/hstr/blob/master/CONFIGURATION.md#bash-binding-hstr-to-keyboard-shortcut
  # https://www.computerhope.com/unix/bash/bind.htm
  #I'm still not so clear on whether the syntax is case sensitive.
  #https://groups.google.com/g/comp.unix.shell/c/UfAkvZ1C10I/m/7Mb4m7DHBgAJ
  #bind -x '"\er": trap '' 2; READLINE_LINE=$(percol_sel_log_history) READLINE_POINT=; trap 2'
  bind -x '"\er": trap '' 2; READLINE_LINE=$(percol_sel_log_history); READLINE_POINT=${#READLINE_LINE}; trap 2'
  
  #https://www.commandlinefu.com/commands/view/24403/make-m-r-run-the-contents-of-the-readline-line-buffer-and-replace-it-with-the-result-in-bash
  # Make M-r run the contents of the Readline line buffer and replace it with the result in Bash
  #bind -x '"\er":READLINE_LINE=$(eval "$READLINE_LINE");READLINE_POINT=${#READLINE_LINE}' 

  #https://www.commandlinefu.com/commands/view/24401/make-m-j-insert-duplicate-the-last-word-of-the-readline-line-buffer-in-bash
  # Make M-j insert (duplicate) the last word of the Readline line buffer in Bash
  #bind '"\ej": "!#:$\e^"' 


  #bind -x '"\C-\M-R": trap '' 2; READLINE_LINE=$(percol_sel_log_master_history) READLINE_POINT=; trap 2'
  #bind -x '"\C-\M-r": trap '' 2; READLINE_LINE=$(percol_sel_log_master_history) READLINE_POINT=; trap 2'
  #bind -x '"\e\C-R": trap '' 2; READLINE_LINE=$(percol_sel_log_master_history) READLINE_POINT=; trap 2'
  #bind -x '"\e\C-r": trap '' 2; READLINE_LINE=$(percol_sel_log_master_history) READLINE_POINT=; trap 2'
fi

# export PROMPT_COMMAND='ar_result=$__bp_last_ret_value; _ariadne -h -u -e "echo -n $ar_result"' # save only to local log file
#export PROMPT_COMMAND='ar_result=$__bp_last_ret_value; _ariadne -h -u -e "echo -n $ar_result" -m "$ariadne_bash_master_log"' # save to master log file too for multiple pcs (e.g. symlink to a cloud drive)


#https://github.com/cantino/mcfly/blob/fd269640f290ce3344cf5800e16d0e8729e0ff43/mcfly.bash#L59
if [ -z "$PROMPT_COMMAND" ]
then
  PROMPT_COMMAND="ariadne_precmd"
else
  PROMPT_COMMAND="ariadne_precmd;${PROMPT_COMMAND#;}"
fi


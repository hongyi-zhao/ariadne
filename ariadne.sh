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
# source $HOME/.config/bash/ariadne/ariadne.sh
# export PROMPT_COMMAND='_ariadne -h -u '
##

    local script=$FUNCNAME
    local histentrycmd=
    local cwd=
    local extra=
    local text=
    local logfile="$HOME/.bash_log"
    local hostname=
    local histentry=
    local histleader=
    local datetimestamp=
    local histlinenum=
    local username=
    local options=":hyunte:l:"
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
    ${tty:+[$tty] } , ${ip:+[$ip] } , ${extra:+[$extra] }"
    
    # save the entry in a logfile
    echo "$histentrycmd" >> $logfile || echo "$script: file error." ; return 1

} 

# modified from https://github.com/mooz/percol#zsh-history-search

function get_seperator() {
    while read i
    do
        re='FIELD_SEP[^#]*#?'
        if [[ $i =~ $re ]]; then
            matching_line=${BASH_REMATCH[0]}
            re="'(.+)'"
            [[ $matching_line =~ $re ]] && SEP=${BASH_REMATCH[1]}
            return 0
        fi
    done < $1
}

function percol_sel_log_history() {
    unset SEP
    get_seperator ${HOME}/.config/bash/ariadne/rc.py
    RCFILE="$HOME/.config/bash/ariadne/rc.py"
    PERCOL="$HOME/.config/bash/ariadne/bin/percol"
    FIELD_SEP=$(get_seperator "$HOME/.oh-my-zsh/custom/ariadne/rc.py")
    PYTHONPATH="$HOME/.config/basch/ariadne/percol":$PYTHONPATH
    $PERCOL --reverse --rcfile=$RCFILE ~/.bash_log --seperator $FIELD_SEP
}

bind -x '"\C-R": trap '' 2; READLINE_LINE=$(percol_sel_log_history) READLINE_POINT=; trap 2'

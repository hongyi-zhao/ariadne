#!/usr/bin/env bash
unset scriptdir_realpath
unset script_realdirname script_realname
unset script_realbasename script_realextname 
unset script_realpath pkg_realpath

scriptdir_realpath=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)

script_realdirname=$(dirname "$(realpath -e "${BASH_SOURCE[0]}")")
script_realname=$(basename "$(realpath -e "${BASH_SOURCE[0]}")")

script_realbasename=${script_realname%.*}
script_realextname=${script_realname##*.}

script_realpath=$script_realdirname/$script_realname
pkg_realpath=${script_realpath%.*}



#https://github.com/gawells/ariadne
#https://github.com/Genivia/ugrep
#https://github.com/peco/peco


#$ egrep -IinR '\\c' .
#./fish_user_key_bindings.fish:2:	bind \cR ariadne
#./fish_user_key_bindings.fish:3:    bind \c\eR ariadne_master
#./ariadne.sh:219:bind -x '"\C-R": trap '' 2; READLINE_LINE=$(percol_sel_log_history) READLINE_POINT=; trap 2'
#./ariadne.sh:220:bind -x '"\C-\M-R": trap '' 2; READLINE_LINE=$(percol_sel_log_master_history) READLINE_POINT=; trap 2'

ariadne_sh=$script_realdirname/ariadne.sh
history_dir=$HOME/.history
ariadne_bash_log=$history_dir/ariadne-bash-log
#ariadne_bash_master_log=$history_dir/ariadne-bash-master-log

if [ ! -d $history_dir ]; then
  mkdir -p $history_dir
fi

if [ ! -e $ariadne_bash_log ]; then
  touch $ariadne_bash_log
fi

#if [ ! -e $ariadne_bash_master_log ]; then
#  touch $ariadne_bash_master_log
#fi

#https://github.com/pyinstaller/pyinstaller/discussions/6493#discussioncomment-1944421
if [ -e $ariadne_sh ]; then
  export ariadne_bash_log=$HOME/.history/ariadne-bash-log
  #export ariadne_bash_master_log=$HOME/.history/ariadne-bash-master-log
  source $ariadne_sh
fi


# Path to Oh My Fish install.
set -g OMF_PATH "/home/gordon/.local/share/omf"
function fish_log --on-event fish_preexec
  echo $history[1]" ### "(date +'%F %H:%M')" , "(pwd) >> ~/.fish_log
end

function browse_fish_history
  set PERCOL "$HOME/.config/fish/functions/ariadne/bin/percol"
  set RCFILE "$HOME/.config/fish/functions/ariadne/rc.py"
  set SEP " <> "
  gawk -v sep="$SEP" 'BEGIN {FS=" ### "} {\
        ORS=sep; \
        split($(NF),a," , "); \
        print a[1]; \
        print a[2]; \
        ORS="\n"; \
        print $1; \
    }' ~/.fish_log  | eval $PERCOL --reverse --rcfile=$RCFILE
end

if [ -z "$TMPDIR" ]
    set -g TMPDIR /tmp
end

function store_fish_history
	browse_fish_history > $TMPDIR/fish.result 
	and commandline (cat $TMPDIR/fish.result)
	commandline -f repaint
    rm -f $TMPDIR/fish.result
end


# Path to Oh My Fish install.
set -g OMF_PATH "/home/gordon/.local/share/omf"

# Customize Oh My Fish configuration path.
#set -gx OMF_CONFIG "/home/gordon/.config/omf"

# Load oh-my-fish configuration.
# source $OMF_PATH/init.fish

function fish_log --on-event fish_preexec
  echo $history[1]" ### "(date)" , "(pwd) >> ~/.fish_log
end

function browse_log
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


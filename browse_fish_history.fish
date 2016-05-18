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

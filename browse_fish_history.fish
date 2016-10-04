function browse_fish_history
	set PERCOL "$HOME/.config/fish/functions/ariadne/bin/percol"
  	set RCFILE "$HOME/.config/fish/functions/ariadne/rc.py"
  	# read 
  	grep "FIELD_SEP" "$HOME/.config/fish/functions/ariadne/rc.py" \
  		| grep -P "'.+?'" -o | head -n 1 | read FIELD_SEP
  	# remove qoutes
  	set FIELD_SEP (string sub --start 2 --length (math (string length $FIELD_SEP)-2) $FIELD_SEP) 
  	eval $PERCOL --reverse --rcfile=$RCFILE --seperator='$FIELD_SEP' ~/.fish_log
end

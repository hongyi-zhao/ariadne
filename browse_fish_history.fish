function browse_fish_history
	set PERCOL "$HOME/.config/fish/functions/ariadne/bin/percol"
  	set RCFILE "$HOME/.config/fish/functions/ariadne/rc.py"
  	
   #  set FIELD_SEP " <> "
  	# eval $PERCOL --reverse --rcfile=$RCFILE --seperator='$FIELD_SEP' ~/.fish_log
    
  	eval $PERCOL --reverse --rcfile=$RCFILE ~/.fish_log
end

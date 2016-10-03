function browse_fish_history
	set PERCOL "$HOME/.config/fish/functions/ariadne/bin/percol"
  set RCFILE "$HOME/.config/fish/functions/ariadne/rc.py"
  set SEP " <> "
  
  eval $PERCOL --reverse --rcfile=$RCFILE ~/.fish_log
end

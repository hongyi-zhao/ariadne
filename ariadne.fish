function ariadne
	browse_fish_history > $TMPDIR/fish.result 
	and commandline (cat $TMPDIR/fish.result)
	commandline -f repaint
    rm -f $TMPDIR/fish.result
end

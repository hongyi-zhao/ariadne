function ariadne
	browse_fish_history > $XDG_RUNTIME_DIR/fish.result 
	and commandline (cat $XDG_RUNTIME_DIR/fish.result)
	commandline -f repaint
    rm -f $XDG_RUNTIME_DIR/fish.result
end

function ariadne_master
    browse_fish_master_history > $XDG_RUNTIME_DIR/fish.result 
    and commandline (cat $XDG_RUNTIME_DIR/fish.result)
    commandline -f repaint
    rm -f $XDG_RUNTIME_DIR/fish.result
end

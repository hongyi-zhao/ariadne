function fish_log --on-event fish_preexec
    set h1 (tail -n 1 .fish_log | awk 'BEGIN {FS=" ### "}  {print $1}')
    set h2 $history[1]

    if [ $h1 != $h2 ] # check for consecutive duplicates
        echo $history[1]" ### "(date +'%F %H:%M')" ,,"(whoami)","(hostname)" ,"(pwd)" ,"(echo $status) >> ~/.fish_log
        # comment out if not saving to master log (e.g. symlink to cloud file) for multiple pcs:
        echo $history[1]" ### "(date +'%F %H:%M')" ,,"(whoami)","(hostname)" ,"(pwd)" ,"(echo $status) >> ~/.fish_master_log
    end
end
function fish_log --on-event fish_preexec
  echo $history[1]" ### "(date +'%F %H:%M')" ,,"(whoami)","(hostname)" ,"(pwd)" ,"(echo $status) >> ~/.fish_log
end

if [ -z "$TMPDIR" ]
    set -g TMPDIR /tmp
end

echo $TMPDIR

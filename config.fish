# Path to Oh My Fish install.
function fish_log --on-event fish_preexec
  echo $history[1]" ### "(date +'%F %H:%M')" , "(pwd) >> ~/.fish_log
end

if [ -z "$TMPDIR" ]
    set -g TMPDIR /tmp
end



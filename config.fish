function fish_log --on-event fish_preexec
  echo $history[1]" ### "(date +'%F %H:%M')" ,,"(whoami)","(hostname)" ,"(pwd)" ,"(echo $status) >> ~/.fish_log
  # comment out if not saving to master log (e.g. symlink to cloud file) for multiple pcs:
  echo $history[1]" ### "(date +'%F %H:%M')" ,,"(whoami)","(hostname)" ,"(pwd)" ,"(echo $status) >> ~/.fish_master_log

  # TODO: add check for duplicate commands
end


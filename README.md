- [Installation](#installation)
  - [Zsh](#zsh)
  - [Bash](#bash)
  - [Fish](#fish)
- [Key bindings](#keybindigs)
- [Configuration](#configuration)

# ariadne

Ariadne enables comprehensive CLI shell history logging, combined with interactive searching, using a modified version of Masafumi Oyamada's interactive grep tool: percol (https://github.com/mooz/percol). The CLI logging in `bash/zsh` is modified from the following scripts:

- http://stackoverflow.com/questions/945288/saving-current-directory-to-bash-history
- https://gist.github.com/jeetsukumaran/2202879)

If you derive little joy from memorizing the arbitrary incantations and arcana of the unix command line this might be for you. With this you can:

1. Reverse search through previous commands and the paths where they were run
2. Extract either the path or command
3. Filter by current path
4. Filter out duplicate commands
5. Filter by exit status 0
6. Hide/show date, command, path fields in search output
7. Stack commands and save to a script (rerun.sh)
8. Filter by host etc

`Ctrl+R` is captured to replace the default history search to pipe the log file (`~/.<zsh/fish/bash>_log`) through the modified percol fuzzy finder. The log file records time, date, directory, host, exit status and command of every command entered. This makes it easy to retrieve commands in a new project directory based on a similar older project, find a deeply nested project dir by the command etc. I find I need this often when running scientific software in the unix world. Similarly `Ctrl+Alt+R` is mapped to read a master log file, which can be used to record commands on multiple hosts if sym-linked to a file in a cloud sync directory. 

![Current look](https://user-images.githubusercontent.com/11155854/132119584-251c9c38-46be-4416-b32d-8ff214aeb7fa.png)

![image](https://user-images.githubusercontent.com/11155854/132346288-a1210d5f-248d-4f9d-9074-4b23ab42b439.png)

Current (more compact) look. Blue indicates exit status = 0, red ≠ 0.

## Installation
    $ git clone https://github.com/gawells/ariadne
    $ cd ariadne
    
### Zsh

    $ ./setup.py -z

Add the following to `~/.zshrc` 

    source ~/.config/zsh/ariadne/ariadne.zsh
    
### Bash
```shell
# First, download and source the following package in ~/.bashrc:
# https://github.com/rcaloras/bash-preexec
#
# Then add something like the following to ~/.bashrc:
export ariadne_bash_log=$HOME/.history/ariadne-bash-log
# If you also want to save the history to master log:   
#export ariadne_bash_master_log=$HOME/.history/ariadne-bash-master-log
source $script_realdirname/ariadne.sh
```    
### Fish
    
    $ ./setup.py -f
    
Add the contents of `./config.fish` to `~/.config/fish/config.fish`

## Key bindings

- Ctrl+R          : Invoke command history search
- Ctrl+Alt+R      : Invoke command history search on master file 

In ariadne:

- F1,F2,F3        : Hide/show date, execution path and command, respectively
- Enter,Ctrl+m    : Extract command(s)
- Ctrl+d          : Extract path(s)
- Ctrl+b          : Extract path and command, seperated by ';'
- Alt+d          : Filter by current directory
- Alt+u           : Toggle filter for duplicate commands
- Alt+e           : Toggle filter commands with exit staus 0
- Ctrl+SPC        : Select entry (useful for extracting salient commands for future recipes?)
- Ctrl+p          : Push command to stack
- Alt+p           : Pop command from stack
- Ctrl+s          : Save stack (as 'rerun'sh') and exit
- Alt-f           : Switch between normal and regex search 
- Alt-h           : Switch between all hosts and current host (mostly for master file)
- Alt-n           : Cycle through hosts (mostly for master file)

## Configuration

Configuration is specified in [`rc.py`](https://github.com/hongyi-zhao/ariadne/blob/master/rc.py).

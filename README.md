- [Introduction](#introduction)
- [Python packaging and distribution](#Python-packaging-and-distribution)
- [Installation](#installation)
  - [Zsh](#zsh)
  - [Bash](#bash)
  - [Fish](#fish)
- [Configuration](#configuration)


# Introduction

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

![image](https://user-images.githubusercontent.com/11155854/132346682-356498c7-dea1-4e08-a3e0-b3d02061651d.png)


# Python packaging and distribution

Use the packaged approach to avoid being affected by the system’s Python virtual environment, say, pyenv. See [here](https://github.com/pyinstaller/pyinstaller/discussions/6493#discussioncomment-1944421) and [here](https://github.com/Nuitka/Nuitka/issues/1375) for the relevant discussions.

```
#https://stackoverflow.com/questions/63107313/is-there-an-alternative-to-pyinstaller-for-python-3-8
#https://pyoxidizer.readthedocs.io/en/stable/pyoxidizer_comparisons.html

# vx_Freeze
#https://github.com/pyinstaller/pyinstaller/discussions/6493#discussioncomment-1944421
$ pyenv shell datasci
# https://github.com/marcelotduarte/cx_Freeze
$ pip install --upgrade cx_Freeze --pre
# The generated executable is dist/perpol
$ cxfreeze -c bin/percol --packages curses,cmd --target-dir dist

# nuitka
# https://github.com/Nuitka/Nuitka/issues/1375#issuecomment-1010526356
#$ pip  install -U nuitka
#$ nuitka3 --standalone --python-flag=no_site --static-libpython=no bin/percol
#If using on the same machine, the following is enough:
#$ nuitka3 --static-libpython=no bin/percol

# pyinstaller
#https://github.com/pyinstaller/pyinstaller/discussions/6493#discussioncomment-1946217
# The generated executable is dist/perpol/perpol
#$ pip uninstall percol 
#$ pyinstaller --clean --noconfirm --collect-submodules percol --paths . bin/percol
```

# Installation
    $ git clone https://github.com/hongyi-zhao/ariadne
    $ cd ariadne
    
## Zsh

    $ ./setup.py -z

Add the following to `~/.zshrc` 

    source ~/.config/zsh/ariadne/ariadne.zsh
    
## Bash
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
## Fish
    
    $ ./setup.py -f
    
Add the contents of `./config.fish` to `~/.config/fish/config.fish`

# Configuration

See [`rc.py`](https://github.com/hongyi-zhao/ariadne/blob/master/rc.py) for details.

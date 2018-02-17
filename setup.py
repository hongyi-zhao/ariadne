#!env python3
# -*- coding: utf-8 -*-
import argparse
import os
from shutil import copy,copy2,copystat

class Error(OSError):
    pass

# modified from shutil to not be stupid about direcotry already existing
def copytree(src, dst, symlinks=False):
    names = os.listdir(src)
    os.makedirs(dst,exist_ok=True)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except OSError as why:
        # can't copy file access times on Windows
        if why.winerror is None:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def install_zsh():
  home = os.path.expanduser('~')
  ar_home = os.path.expanduser('~/.config/zsh/ariadne')
  os.makedirs("%s/percol"%ar_home,exist_ok=True)
  copy("./ariadne.zsh","%s"%ar_home)
  copy("./rc.py","%s"%ar_home)
  copytree("./percol","%s/percol"%ar_home)
  copytree("./bin","%s/bin"%ar_home)
  copytree("./tools","%s/tools"%ar_home)


def install_bash():
  home = os.path.expanduser('~')
  ar_home = os.path.expanduser('~/.config/bash/ariadne')
  os.makedirs("%s/percol"%ar_home,exist_ok=True)
  copy("./ariadne.sh","%s"%ar_home)
  copy("./rc.py","%s"%ar_home)
  copytree("./percol","%s/percol"%ar_home)
  copytree("./bin","%s/bin"%ar_home)
  copytree("./tools","%s/tools"%ar_home)

def install_fish():
  home = os.path.expanduser('~')
  ar_home = os.path.expanduser('~/.config/fish/functions')
  os.makedirs("%s/percol"%ar_home,exist_ok=True)
  copy("./ariadne.fish","%s"%ar_home)
  copy("./browse_fish_history.fish","%s"%ar_home)
  copy("./fish_user_key_bindings.fish","%s"%ar_home)
  copy("./rc.py","%s/ariadne"%ar_home)
  copytree("./percol","%s/ariadne/percol"%ar_home)
  copytree("./bin","%s/ariadne/bin"%ar_home)
  copytree("./tools","%s/ariadne/tools"%ar_home)


def main():
  parser = argparse.ArgumentParser()  
  parser.add_argument("-z","--zsh",action="store_true",default=False,help="Install for zsh")
  parser.add_argument("-b","--bash",action="store_true",default=False,help="Install for bash")
  parser.add_argument("-f","--fish",action="store_true",default=False,help="Install for fish")

  args = parser.parse_args()

  if args.zsh:
    install_zsh()

  if args.bash:
    install_bash()

  if args.fish:
    install_fish()

if __name__ == '__main__':
  main()


#probably don't need this atm - gw
#!/usr/bin/env python

# from setuptools import setup

# exec(open("percol/info.py").read())

# setup(name             = "percol",
#       version          = __version__,
#       author           = "mooz",
#       author_email     = "stillpedant@gmail.com",
#       url              = "https://github.com/mooz/percol",
#       description      = "Adds flavor of interactive filtering to the traditional pipe concept of shell",
#       long_description = __doc__,
#       packages         = ["percol"],
#       scripts          = ["bin/percol"],
#       classifiers      = ["Environment :: Console :: Curses",
#                           "License :: OSI Approved :: MIT License",
#                           "Operating System :: POSIX",
#                           "Programming Language :: Python",
#                           "Topic :: Text Processing :: Filters",
#                           "Topic :: Text Editors :: Emacs",
#                           "Topic :: Utilities"],
#       keywords         = "anything.el unite.vim dmenu shell pipe filter curses",
#       license          = "MIT",
#       install_requires = ["six >= 1.7.3", "cmigemo >= 0.1.5"]
#       )



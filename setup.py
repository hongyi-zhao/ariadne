#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#https://discuss.python.org/t/setup-py-error-unrecognized-arguments-egg-info-egg-base-tmp-pip-pip-egg-info-nx929i7g/14005/6?u=hongyi-zhao
#https://github.com/mooz/percol/blob/master/setup.py
#$ virtualenv venv 
#$ venv/bin/pip install -U pip
#$ venv/bin/pip install .

from setuptools import setup

exec(open("percol/info.py").read())

setup(name             = "percol",
      version          = __version__,
      author           = "mooz",
      author_email     = "stillpedant@gmail.com",
      url              = "https://github.com/mooz/percol",
      description      = "Adds flavor of interactive filtering to the traditional pipe concept of shell",
      long_description = __doc__,
      packages         = ["percol"],
      scripts          = ["bin/percol"],
      classifiers      = ["Environment :: Console :: Curses",
                          "License :: OSI Approved :: MIT License",
                          "Operating System :: POSIX",
                          "Programming Language :: Python",
                          "Topic :: Text Processing :: Filters",
                          "Topic :: Text Editors :: Emacs",
                          "Topic :: Utilities"],
      keywords         = "anything.el unite.vim dmenu shell pipe filter curses",
      license          = "MIT",
      install_requires = ["six >= 1.7.3", "cmigemo >= 0.1.5"]
      )

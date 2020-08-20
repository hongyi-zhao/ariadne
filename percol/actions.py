# -*- coding: utf-8 -*-

import sys, six

from percol.action import action

def double_quote_string(string):
    return '"' + string.replace('"', r'\"') + '"'

def get_raw_stream(stream):
    if six.PY2:
        return stream
    else:
        return stream.buffer

@action()  # the point of this is to convert a function to a class instance / object?
def output_to_stdout(lines, percol):
    "output marked (selected) items to stdout" # this is ending up in the results output, what for?
    stdout = get_raw_stream(sys.stdout)
    for line in lines:
        stdout.write(percol.display.get_raw_string(line))
        stdout.write(six.b("\n"))

@action()
def output_to_stdout_double_quote(lines, percol):
    "output marked (selected) items to stdout with double quotes"
    stdout = get_raw_stream(sys.stdout)
    for line in lines:
        stdout.write(percol.display.get_raw_string(double_quote_string(line)))
        stdout.write(six.b("\n"))

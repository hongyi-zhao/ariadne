# -*- coding: utf-8 -*-
import sys
import os
import locale
import six
import re

from optparse import OptionParser

import percol
from percol import Percol
from percol import tty
from percol import debug
from percol import ansi
from percol import command

FIELD_SEP = '║'
INSTRUCTION_TEXT = ansi.markup("""<bold><blue>{logo}</blue></bold>
                                <on_blue><underline> {version} </underline></on_blue>

You did not give any inputs to <underline>percol</underline>. Check following typical usages and try again.

<underline>(1) Giving a filename,</underline>

 $ <underline>percol</underline> /var/log/syslog

<underline>(2) or specifying a redirection.</underline>

 $ ps aux | <underline>percol</underline>

""").format(logo = percol.__logo__,
            version = percol.__version__)

class LoadRunCommandFileError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return "Error in rc.py: " + str(self.error)

CONF_ROOT_DIR = os.path.expanduser("~/.percol.d/")
DEFAULT_CONF_PATH = CONF_ROOT_DIR + "rc.py"

def create_default_rc_file():
    if not os.path.exists(CONF_ROOT_DIR):
        os.makedirs(CONF_ROOT_DIR)
    with open(DEFAULT_CONF_PATH, "w+") as file:
        file.write("# Run command file for percol\n")

def load_rc(percol, path = None, encoding = 'utf-8'):
    if path is None:
        if not os.path.exists(DEFAULT_CONF_PATH):
            create_default_rc_file()
        path = DEFAULT_CONF_PATH
    try:
        with open(path, "rb") as file:
            exec(compile(file.read(), path, 'exec'), locals())
    except Exception as e:
        raise LoadRunCommandFileError(e)

def eval_string(percol, string_to_eval, encoding = 'utf-8'):
    try:
        import six
        if not isinstance(string_to_eval, six.text_type):
            string_to_eval = string_to_eval.decode(encoding)
        exec(string_to_eval, locals())
    except Exception as e:
        debug.log("cli.py, Exception in eval_string", e)

def error_message(message):
    return ansi.markup("<bold><on_red><white>[Error]</white></on_red></bold> " + message)

def setup_options(parser):
    parser.add_option("--tty", dest = "tty",
                      help = "path to the TTY (usually, the value of $TTY)")
    parser.add_option("--rcfile", dest = "rcfile",
                      help = "path to the settings file")
    parser.add_option("--output-encoding", dest = "output_encoding",
                      help = "encoding for output")
    parser.add_option("--input-encoding", dest = "input_encoding", default = "utf8",
                      help = "encoding for input and output (default 'utf8')")
    parser.add_option("-v", "--invert-match", action="store_true", dest = "invert_match", default = False,
                      help = "select non-matching lines")
    parser.add_option("--query", dest = "query",
                      help = "pre-input query")
    parser.add_option("--eager", action = "store_true", dest = "eager", default = False,
                      help = "suppress lazy matching (slower, but display correct candidates count)")
    parser.add_option("--eval", dest = "string_to_eval",
                      help = "eval given string after loading the rc file")
    parser.add_option("--prompt", dest = "prompt", default = None,
                      help = "specify prompt (percol.view.PROMPT)")
    parser.add_option("--right-prompt", dest = "right_prompt", default = None,
                      help = "specify right prompt (percol.view.RPROMPT)")
    parser.add_option("--match-method", dest = "match_method", default = "",
                      help = "specify matching method for query. `string` (default) and `regex` are currently supported")
    parser.add_option("--caret-position", dest = "caret",
                       help = "position of the caret (default length of the `query`)")
    parser.add_option("--initial-index", dest = "index",
                      help = "position of the initial index of the selection (numeric, \"first\" or \"last\")")
    parser.add_option("--case-sensitive", dest = "case_sensitive", default = False, action="store_true",
                      help = "whether distinguish the case of query or not")
    parser.add_option("--reverse", dest = "reverse", default = False, action="store_true",
                      help = "whether reverse the order of candidates or not")
    parser.add_option("--auto-fail", dest = "auto_fail", default = False, action="store_true",
                      help = "auto fail if no candidates")
    parser.add_option("--auto-match", dest = "auto_match", default = False, action="store_true",
                      help = "auto matching if only one candidate")

    parser.add_option("--prompt-top", dest = "prompt_on_top", default = None, action="store_true",
                      help = "display prompt top of the screen (default)")
    parser.add_option("--prompt-bottom", dest = "prompt_on_top", default = None, action="store_false",
                      help = "display prompt bottom of the screen")
    parser.add_option("--result-top-down", dest = "results_top_down", default = None, action="store_true",
                      help = "display results top down (default)")
    parser.add_option("--result-bottom-up", dest = "results_top_down", default = None, action="store_false",
                      help = "display results bottom up instead of top down")

    parser.add_option("--quote", dest = "quote", default = False, action="store_true",
                      help = "whether quote the output line")
    parser.add_option("--peep", action = "store_true", dest = "peep", default = False,
                      help = "exit immediately with doing nothing to cache module files and speed up start-up time")

    parser.add_option("--seperator", dest='seperator')

    parser.add_option('--host', dest='host')

def set_proper_locale(options):
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    if options.output_encoding:
        output_encoding = options.output_encoding
    return output_encoding

def join_tuple(tup):
    result = ''
    for t in tup:
        result = result+str(t)+','
    return result

# def read_input(filename, encoding, reverse=False):
def read_input(filename, encoding, reverse=False, seperator=''):
    import codecs
    if filename:
        if six.PY2:
            stream = codecs.getreader(encoding)(open(filename, "r"), "replace")
        else:
            stream = open(filename, "r", encoding=encoding)
    else:
        if six.PY2:
            stream = codecs.getreader(encoding)(sys.stdin, "replace")
        else:
            import io
            stream = io.TextIOWrapper(sys.stdin.buffer, encoding=encoding)
    if reverse:
        lines = reversed(stream.readlines())
    else:
        lines = stream

    # preprocess lines into "date-time <sep> path <sep> command" for ariadne
    # previously done with awk in shell scripts, but slows things down a bit
    for line in lines:
        arr = line.split('###')
        # check for malformed entry
        if len(arr) == 2:
            cmd = arr[0].rstrip()
            meta_data_arr = arr[1].strip().split(',')
            if len(meta_data_arr) > 0:
                date = meta_data_arr[0]
                date = date.strip()

                host = meta_data_arr[3]
                host = host.strip()
                
                path = meta_data_arr[4]
                path = path.strip()
                path.replace(' ','\\\\ ')
                
                out_line = date+seperator+path+seperator+cmd
                out_line = ansi.remove_escapes(out_line.rstrip("\r\n"))
                
                # exit status = -999 if non-int string or empty
                try: 
                    exit_status = int(meta_data_arr[-1])
                except ValueError:
                    exit_status = -999
                
                tup = (out_line,exit_status,host)
                
                yield tup
                # debug.log(tup)


    stream.close()

def decide_match_method(options):
    if options.match_method == "regex":
        from percol.finder import FinderMultiQueryRegex
        return FinderMultiQueryRegex
    elif options.match_method == "migemo":
        from percol.finder import FinderMultiQueryMigemo
        return FinderMultiQueryMigemo
    elif options.match_method == "pinyin":
        from percol.finder import FinderMultiQueryPinyin
        return FinderMultiQueryPinyin
    else:
        from percol.finder import FinderMultiQueryString
        return FinderMultiQueryString

def main():
    from percol import __version__
    parser = OptionParser(usage = "Usage: %prog [options] [FILE]", version = "%prog {0}".format(__version__))
    setup_options(parser)
    options, args = parser.parse_args()

    if options.peep:
        sys.exit(1)

    def exit_program(msg = None, show_help = True):
        if not msg is None:
            print(msg)
        if show_help:
            parser.print_help()
        sys.exit(1)

    # get ttyname
    ttyname = options.tty or tty.get_ttyname()
    if not ttyname:
        exit_program(error_message("""No tty name is given and failed to guess it from descriptors.
Maybe all descriptors are redirected."""))

    # decide which encoding to use
    output_encoding = set_proper_locale(options)
    input_encoding = options.input_encoding

    def open_tty(ttyname):
        if six.PY2:
            return open(ttyname, "r+w")
        else:
            # See https://github.com/stefanholek/term/issues/1
            return open(ttyname, "wb+", buffering=0)

    with open_tty(ttyname) as tty_f:
        if not tty_f.isatty():
            exit_program(error_message("{0} is not a tty file".format(ttyname)),
                         show_help = False)

        filename = args[0] if len(args) > 0 else None

        if filename and not os.access(filename, os.R_OK):
            exit_program(error_message("Cannot read a file '" + filename + "'"),
                         show_help=False)

        if filename is None and sys.stdin.isatty():
            tty_f.write(INSTRUCTION_TEXT.encode(output_encoding))
            exit_program(show_help = False)

        # read input

        # TODO: make sure works without rc file specified
        if options.seperator is not None:            
            # debug.log("Percol here")
            FIELD_SEP = options.seperator
        else:
            with open(options.rcfile) as f:
                for line in f:
                    if re.search('^FIELD_SEP\s+=\s+',line):
                        r = re.search('\'(?P<sep>.+?)\'',line)
                        FIELD_SEP = r.group('sep')
                        # debug.log(f"Percol cli.py {FIELD_SEP}")
                        break

        try:
            # candidates = read_input(filename, input_encoding, reverse=options.reverse)
            candidates = read_input(filename, input_encoding, reverse=options.reverse, seperator=FIELD_SEP)
            # candidates,exit_codes = read_input(filename, input_encoding, reverse=options.reverse, seperator=options.seperator)
        except KeyboardInterrupt:
            exit_program("Canceled", show_help = False)

        # setup actions
        import percol.actions as actions
        if (options.quote):
            acts  = (actions.output_to_stdout_double_quote, )
        else:
            acts  = (actions.output_to_stdout, actions.output_to_stdout_double_quote)

        # arrange finder class
        candidate_finder_class = action_finder_class = decide_match_method(options)

        def set_finder_attribute_from_option(finder_instance):
            finder_instance.lazy_finding = not options.eager
            finder_instance.case_insensitive = not options.case_sensitive
            finder_instance.invert_match = options.invert_match

        def set_if_not_none(src, dest, name):
            value = getattr(src, name)
            if value is not None:
                setattr(dest, name, value)

        myhost = os.uname()[1] # get hostname for left prompt
        myhost = myhost.strip()

        with Percol(descriptors = tty.reconnect_descriptors(tty_f),
                    candidates = candidates,
                    actions = acts ,
                    finder = candidate_finder_class,
                    action_finder = action_finder_class,
                    query = options.query,
                    caret = options.caret,
                    index = options.index,
                    encoding = output_encoding,
                    host = myhost,
                    field_sep = FIELD_SEP) as percol:
            # load run-command file
            load_rc(percol, options.rcfile)
            
            # seperator can now be set via command-line. Does not work here for setting FIELD_SEP to convert the log_file to separated output, moved up
            if options.seperator is not None:
                percol.view.__class__.FIELD_SEP = property(lambda self: options.seperator)
                percol.command.set_field_sep(options.seperator)
            else:                
                percol.view.__class__.FIELD_SEP = FIELD_SEP                
                percol.command.set_field_sep(FIELD_SEP)
            
            # override prompts
            if options.prompt is not None:
                percol.view.__class__.PROMPT = property(lambda self: options.prompt)
            if options.right_prompt is not None:
                percol.view.__class__.RPROMPT = property(lambda self: options.right_prompt)

            # evalutate strings specified by the option argument
            if options.string_to_eval is not None:
                eval_string(percol, options.string_to_eval, locale.getpreferredencoding())
            # finder settings from option values
            set_finder_attribute_from_option(percol.model_candidate.finder)
            debug.log(f'cli.py: {percol.model.finder.host}')
            # percol.model.finder.host = 'greyarea'
            # view settings from option values
            set_if_not_none(options, percol.view, 'prompt_on_top')
            set_if_not_none(options, percol.view, 'results_top_down')
            # enter main loop
            if options.auto_fail and percol.has_no_candidate():
                exit_code = percol.cancel_with_exit_code()
            elif options.auto_match and percol.has_only_one_candidate():
                exit_code = percol.finish_with_exit_code()
            else:
                exit_code = percol.loop()

            if exit_code == 10:
                stack = [s+'\n' for s in percol.model.stack]
                # outfilename = input("Script file name: ")
                # print(outfilename)
                # outfile = open(outfilename,'w')
                # outfile.writelines(stack)
                # outfile.close()

        sys.exit(exit_code)

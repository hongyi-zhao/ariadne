# -*- coding: utf-8 -*-

# ============================================================ #
# Action
# ============================================================ #

class Action(object):
    def __init__(self, desc, act, args):
    # def __init__(self, act, args):
        self.act  = act
        self.desc = desc
        self.args = args

def action(**args):
    def act_handler(act):
        return Action(act.__doc__, act, args)
        # return Action(act, args)
    return act_handler

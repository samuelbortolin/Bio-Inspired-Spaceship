from functools import partial

import gamerun


class AgentSimulator(object):

    def __init__(self):
        self.keys = {
            gamerun.K_LEFT: False,
            gamerun.K_RIGHT: False,
            gamerun.K_SPACE: False
        }

    def action_left(self):
        self.keys[gamerun.K_LEFT] = True
        self.keys[gamerun.K_RIGHT] = False
        self.keys[gamerun.K_SPACE] = False

    def action_left_and_fire(self):
        self.keys[gamerun.K_LEFT] = True
        self.keys[gamerun.K_RIGHT] = False
        self.keys[gamerun.K_SPACE] = True

    def action_still(self):
        self.keys[gamerun.K_LEFT] = False
        self.keys[gamerun.K_RIGHT] = False
        self.keys[gamerun.K_SPACE] = False

    def action_still_and_fire(self):
        self.keys[gamerun.K_LEFT] = False
        self.keys[gamerun.K_RIGHT] = False
        self.keys[gamerun.K_SPACE] = True

    def action_right(self):
        self.keys[gamerun.K_LEFT] = False
        self.keys[gamerun.K_RIGHT] = True
        self.keys[gamerun.K_SPACE] = False

    def action_right_and_fire(self):
        self.keys[gamerun.K_LEFT] = False
        self.keys[gamerun.K_RIGHT] = True
        self.keys[gamerun.K_SPACE] = True

    def run(self, routine):
        if callable(routine):
            routine()
            

def progn(*args):
    for arg in args:
        if callable(arg):
            arg()


def exec2(out1, out2):
    return partial(progn, out1, out2)


def exec3(out1, out2, out3):
    return partial(progn, out1, out2, out3)


def prog_while(condition, f):
    if callable(condition):
        while condition():
            if callable(f):
                f()


def exec_while(condition, f):
    return partial(prog_while, condition, f)


def if_then_else(condition, out1, out2):
    if callable(condition):
        if condition():
            if callable(out1):
                out1()
        else:
            if callable(out2):
                out2()


def exec_if_then_else(condition, out1, out2):
    return partial(if_then_else, condition, out1, out2)

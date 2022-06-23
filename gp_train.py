import gamerun


class Output:
    pass


class A(Output):
    pass


class B(Output):
    pass


class C(Output):
    pass


class D(Output):
    pass


class E(Output):
    pass


class F(Output):
    pass


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

    def run(self, routine, *args):
        output = routine(*args)
        self.keys[gamerun.K_LEFT] = output == A or output == B
        self.keys[gamerun.K_RIGHT] = output == E or output == F
        self.keys[gamerun.K_SPACE] = output == A or output == C or output == E


def eval_function(f):
    return f()


def laser_distance():
    min_d = 9999999
    for x, y in zip(gamerun.laser_x, gamerun.laser_y):
        min_d = min(min_d, (gamerun.battleship.x - x)**2 + (gamerun.battleship.y - y)**2)
    return min_d


def exec2(out1, out2):
    out1()
    out2()
    return 0


def exec3(out1, out2, out3):
    out1()
    out2()
    out3()
    return 0


def if_then_else(condition, out1, out2):
    return out1 if condition else out2

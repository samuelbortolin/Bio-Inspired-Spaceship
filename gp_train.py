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
        direction = routine(
            gamerun.battleship.x,
            gamerun.battleship.vel,
            # gamerun.battleship.health,
            gamerun.aliens_x[0],
            gamerun.aliens_x[1],
            gamerun.laser_x[0],
            gamerun.laser_y[0],
            gamerun.laser_x[1],
            gamerun.laser_y[1],
            gamerun.laser_x[2],
            gamerun.laser_y[2],
            gamerun.laser_x[3],
            gamerun.laser_y[3],
            gamerun.laser_x[4],
            gamerun.laser_y[4],
            gamerun.laser_x[5],
            gamerun.laser_y[5],
            gamerun.enemy_spaceships_x[0]
        )

        self.keys[gamerun.K_LEFT] = direction
        self.keys[gamerun.K_RIGHT] = not direction
        self.keys[gamerun.K_SPACE] = True


def eval_function(f):
    return f()

def laser_distance():
    min_d = 9999999
    for x,y in zip(gamerun.laser_x, gamerun.laser_y):
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


# def exec_if_then_else(condition, out1, out2):
#     return partial(if_then_else, condition, out1, out2)

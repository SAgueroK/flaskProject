from multiprocessing import Pipe, Pool

import app
from State2NN import AI_Board


class MulEnvs(object):
    game = AI_Board()
    count = 1

    def __init__(self, process_num):
        self.process_num = process_num

    def next(self, Actions):
        Images, Rewards, Isdones = [], [], []
        image, reward, isdone = self.game.next(Actions[0])
        reward_file = app.rewards_file(time=self.count, rewards=reward)
        self.count += 1
        app.insert_rewards(reward_file)
        Images.append(image)
        Rewards.append(reward)
        Isdones.append(isdone)
        return Images, Rewards, Isdones

    def game_exit(self):
        self.game.self_quit()

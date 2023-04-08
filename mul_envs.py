from multiprocessing import Pipe, Pool
from State2NN import AI_Board
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
reward_list = []
action_list = []


def run_game(child_conn):
    game = AI_Board()
    isdone = False
    while True:
        action = child_conn.recv()  # 队列为空时会阻塞进程
        if action != 999:
            print('-[INFO] get action:{} from queue'.format(action))
            image, reward, isdone = game.next(action)
            reward_list.append(reward)
            action_list.append(action)
            if isdone:
                game.reset()
            child_conn.send([image, reward, isdone])

        else:
            step_list = []
            for step in range(0, len(reward_list)):
                step_list.append(step)
            c = (
                Line()
                .add_xaxis(step_list)
                .add_yaxis("奖励值", reward_list)
                .set_global_opts(title_opts=opts.TitleOpts(title="折线图-奖励值"))
                .render("./templates/line_reward.html")
            )
            game.self_quit()
            break



class MulEnvs(object):

    def __init__(self, process_num):
        self.process_num = process_num
        self.init_process()

    def init_process(self):
        self.Process_Pool = Pool(self.process_num)
        self.Parent_Conns, self.Child_Conns = zip(
            *[Pipe() for _ in range(self.process_num)])
        for id_ in range(self.process_num):
            # 创建process_num个游戏进程
            self.Process_Pool.apply_async(
                run_game, args=(self.Child_Conns[id_],))

    def next(self, Actions):
        Images, Rewards, Isdones = [], [], []
        for id_ in range(self.process_num):
            self.Parent_Conns[id_].send(Actions[id_])

        for id_ in range(self.process_num):
            image, reward, isdone = self.Parent_Conns[id_].recv()
            print(
                '-[INFO] id_{} get action: from queue, reward:{}'.format(id_, reward))
            Images.append(image)
            Rewards.append(reward)
            Isdones.append(isdone)

        return Images, Rewards, Isdones

    def game_exit(self):
        for id_ in range(self.process_num):
            self.Parent_Conns[id_].send(999)

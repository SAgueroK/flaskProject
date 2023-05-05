import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from xpinyin import Pinyin
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import train_mul
from concurrent.futures import ThreadPoolExecutor
import datetime
import json

executor = ThreadPoolExecutor()
app = Flask(__name__)
# MySQL所在主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，自己设置
USERNAME = "root"
# 连接MySQL的密码，自己设置
PASSWORD = "heyadi"
# MySQL上创建的数据库名称
DATABASE = "bishe"
# 通过修改以下代码来操作不同的SQL比写原生SQL简单很多 --》通过ORM可以实现从底层更改使用的SQL
# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}" \
                                        f"?charset=utf8"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds=1)

db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def main():  # put application's code here
    return render_template('./login.html')


@app.route('/try_login')
def try_login():  # put application's code here
    name = str(request.args.get("name"))
    password = str(request.args.get("password"))
    user = db.session.query(User).filter_by(name=name).first()
    print(name, password)
    if user is None:
        return render_template('./login.html')
    if (name != user.name) or (password != user.password):
        return render_template('./login.html')
    else:
        return render_template('./index.html', username=name)


@app.route('/login')
def login():  # put application's code here
    return render_template('./login.html')


@app.route('/show')
def show():  # put application's code here
    username = str(request.args.get("username"))
    model_files = get_model_files(username)
    return render_template('./show.html', username=username, model_files=model_files)


@app.route('/use')
def use():  # put application's code here
    username = str(request.args.get("username"))
    model_files = get_model_files(username)
    return render_template('./use.html', username=username, model_files=model_files)


@app.route('/result_chart')
def result_chart():
    username = str(request.args.get("username"))
    model_files = get_model_files(username)
    return render_template('./result_chart.html', username=username, model_files=model_files)


def transit(data):
    res = []
    for x in data:
        res.append(int(x))
    return res


@app.route('/result_compare_chart')
def line_reward():  # put application's code here
    username = str(request.args.get("username"))
    p = Pinyin()
    len = 0
    rewards_file = get_rewards_file()
    content = []
    line = Line()
    modelfiles = [Model_file() for _ in range(5)]
    size = 0
    line.set_global_opts(title_opts=opts.TitleOpts(title="对比图"), xaxis_opts=opts.AxisOpts(name="时间轴"), yaxis_opts=
    opts.AxisOpts(name="奖励值"), legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=30)))
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    ax = []
    for x in rewards_file:
        ax.append(len)
        len += 1
    tmp = []
    if str(request.args.get("load_name_1")) != "0":
        name = p.get_pinyin(str(request.args.get("load_name_1")))
        load_name_1 = username + name
        file1 = open("rewards_data\\" + load_name_1 + ".txt", 'r')
        content1 = transit(file1.readline().split())
        for i in range(len):
            tmp.append([ax[i], content1[i]])
        content.append(tmp)
        file1.close()  # 文件打开，使用完毕后需要关闭
        modelfiles[size] = get_model_file(name)
        size += 1
    if str(request.args.get("load_name_2")) != "0":
        name = p.get_pinyin(str(request.args.get("load_name_2")))
        load_name_2 = username + name
        file2 = open("rewards_data\\" + load_name_2 + ".txt", 'r')
        content2 = transit(file2.readline().split())
        tmp = []
        for i in range(len):
            tmp.append([ax[i], content2[i]])
        content.append(tmp)
        file2.close()  # 文件打开，使用完毕后需要关闭
        modelfiles[size] = get_model_file(name)
        size += 1
    if str(request.args.get("load_name_3")) != "0":
        name = p.get_pinyin(str(request.args.get("load_name_3")))
        load_name_3 = username + name
        file3 = open("rewards_data\\" + load_name_3 + ".txt", 'r')
        content3 = transit(file3.readline().split())
        tmp = []
        for i in range(len):
            tmp.append([ax[i], content3[i]])
        content.append(tmp)
        file3.close()  # 文件打开，使用完毕后需要关闭
        modelfiles[size] = get_model_file(name)
        size += 1
    if str(request.args.get("load_name_4")) != "0":
        name = p.get_pinyin(str(request.args.get("load_name_4")))
        load_name_4 = username + name
        file4 = open("rewards_data\\" + load_name_4 + ".txt", 'r')
        content4 = transit(file4.readline().split())
        tmp = []
        for i in range(len):
            tmp.append([ax[i], content4[i]])
        content.append(tmp)
        file4.close()  # 文件打开，使用完毕后需要关闭
        modelfiles[size] = get_model_file(name)
        size += 1
    if str(request.args.get("load_name_5")) != "0":
        name = p.get_pinyin(str(request.args.get("load_name_5")))
        load_name_5 = username + name
        file5 = open("rewards_data\\" + load_name_5 + ".txt", 'r')
        content5 = transit(file5.readline().split())
        tmp = []
        for i in range(len):
            tmp.append([ax[i], content5[i]])
        content.append(tmp)
        file5.close()  # 文件打开，使用完毕后需要关闭
        modelfiles[size] = get_model_file(name)
        size += 1
    supple = size
    while supple < 5:
        tmp = []
        supple += 1
        content.append(tmp)
    print(content[3])
    return render_template('./result_compare_chart.html', modelfiles=modelfiles, size=size, content=content)


@app.route('/line_score')
def line_score():  # put application's code here
    return render_template('./line_score.html')


@app.route('/bar_action_count')
def bar_action_count():  # put application's code here
    return render_template('./bar_action_count.html')


@app.route('/position_action_time')
def position_action_time():  # put application's code here
    return render_template('./position_action_time.html')


@app.route('/train', methods=["GET"])
def train():  # put application's code here
    delete_rewards()
    p = Pinyin()
    username = str(request.args.get("username"))
    save_name = str(request.args.get("save_name"))
    if save_name == "None":
        save_name = str(request.args.get("load_name"))
    save_path = './final/{}.ckpt'.format(username + p.get_pinyin(save_name))
    model_file = db.session.query(Model_file).filter_by(name=save_name).first()
    if model_file is not None:
        delete_model_file(model_file)
    learn_factor = int(request.args.get("learn_factor"))
    memory_warmup_size = int(request.args.get("memory_warmup_size"))
    batch_size = int(request.args.get("batch_size"))
    learning_rate = float(request.args.get("learning_rate"))
    gamma = float(request.args.get("gamma"))
    functions = str(request.args.get("functions"))
    hid1_size = int(request.args.get("hid1_size"))
    hid2_size = int(request.args.get("hid2_size"))
    observation = float(request.args.get("observation"))
    model_file = Model_file(user_name=username, name=save_name, path=save_path, learn_factor=learn_factor,
                            memory_warmup_size=memory_warmup_size, batch_size=batch_size, learning_rate=learning_rate,
                            gamma=gamma, functions=functions, hid1_size=hid1_size, hid2_size=hid2_size,
                            observation=observation)
    insert_model_file(model_file)
    run(
        learn_factor=learn_factor,
        memory_warmup_size=memory_warmup_size,
        batch_size=batch_size,
        learning_rate=learning_rate,
        gamma=gamma,
        functions=functions,
        hid1_size=hid1_size,
        hid2_size=hid2_size,
        load_name=str(request.args.get("load_name")),
        save_name=save_name,
        username=username,
        observation=observation
    )
    rewards_file = get_rewards_file()
    filename = "rewards_data\\" + save_path.split('/')[-1].split('.')[0] + ".txt"
    file = open(filename, 'w')
    file.write('')
    file = open(filename, 'a')
    index = 0
    for tmp in rewards_file:
        index += 1
        if index != rewards_file.__len__():
            file.write(tmp.rewards + ' ')
        else:
            file.write(tmp.rewards)
    return redirect(url_for('show', model_file=model_file))


@app.route('/register')
def register():
    return render_template('./register.html')


@app.route('/echart')
def echart():
    return render_template('./echart.html')


@app.route('/try_register')
def try_register():  # put application's code here
    name = str(request.args.get("name"))
    password = str(request.args.get("password"))
    print(name, password)
    us1 = User(name=name, password=password)
    db.session.add(us1)
    db.session.commit()
    return render_template('./login.html')


@app.route('/chart_reward')
def chart_reward():
    return render_template('./register.html')


@app.route('/get_rewards')
def get_rewards():  # put application's code here
    reward_lists = get_rewards_file()
    data = []
    for reward in reward_lists:
        reward.__dict__.pop("_sa_instance_state")
        data.append(reward.__dict__)
    return json.dumps(data)


@app.route('/demo')
def demo():  # put application's code here
    delete_rewards()
    return render_template('./login.html')


def run(learn_factor, memory_warmup_size, batch_size, learning_rate, gamma, functions, hid1_size, hid2_size,
        load_name, save_name, username, observation):
    print("app:", learn_factor, memory_warmup_size, batch_size, learning_rate, gamma, functions, hid1_size,
          hid2_size, load_name, save_name, username, observation)
    p = Pinyin()
    save_path = './final/{}.ckpt'.format(username + p.get_pinyin(save_name))
    if load_name is not "0":
        load_path = './final/{}.ckpt'.format(username + p.get_pinyin(load_name))
    else:
        load_path = load_name

    train_mul_instance = train_mul
    train_mul_instance.set_factor(learn_factor, memory_warmup_size, batch_size, learning_rate, gamma,
                                  hid1_size, hid2_size, load_path, save_path, observation)
    train_mul_instance.run(functions)


class User(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'user'
    #  字段
    name = db.Column(db.String(255), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)


class Model_file(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'model_file'
    #  字段
    user_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    learn_factor = db.Column(db.String(255), nullable=False)
    memory_warmup_size = db.Column(db.String(255), nullable=False)
    batch_size = db.Column(db.String(255), nullable=False)
    learning_rate = db.Column(db.String(255), nullable=False)
    gamma = db.Column(db.String(255), nullable=False)
    functions = db.Column(db.String(255), nullable=False)
    hid1_size = db.Column(db.String(255), nullable=False)
    hid2_size = db.Column(db.String(255), nullable=False)
    observation = db.Column(db.String(255), nullable=False)


class rewards_file(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'rewards'
    #  字段
    time = db.Column(db.String(255), nullable=False, primary_key=True)
    rewards = db.Column(db.String(255), nullable=False)


def get_rewards_file():
    rewards_files = db.session.query(rewards_file).all()
    return rewards_files


def get_model_files(username):
    model_files = db.session.query(Model_file).filter_by(user_name=username).all()
    return model_files


def get_model_file(name):
    model_files = db.session.query(Model_file).filter_by(name=name).first()
    return model_files


def insert_model_file(model_file):
    db.session.add(model_file)
    db.session.commit()


def delete_model_file(model_file):
    db.session.delete(model_file)
    db.session.commit()


def delete_rewards():
    rewards_files = db.session.query(rewards_file).all()
    for reward in rewards_files:
        db.session.delete(reward)
    db.session.commit()


def insert_rewards(reward):
    db.session.add(reward)
    db.session.commit()


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=8090)

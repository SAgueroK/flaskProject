import os
import datetime

from pyecharts.charts import Line

from pyecharts import options as opts

def write(filename, content):
    # 打开文件并写入内容
    file = open(filename, 'a')
    file.write(content)


def read(filename):
    file1 = open(filename, 'r')
    content1 = file1.readlines()
    print(content1)
    file1.close()  # 文件打开，使用完毕后需要关闭


if __name__ == '__main__':


    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 10, 100]
    v2 = [55, 60, 16, 20, 15, 80]
    line = Line()
    line.set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
    line.add("商家A", attr, v1, mark_point=["average"])
    line.add("商家B", attr, v2, is_smooth=True, mark_line=["max", "average"])
    line.render()

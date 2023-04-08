import os

from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.faker import Faker


if __name__ == '__main__':
    list = []
    for step in range(0,50):
        list.append(step)
    c = (
        Line()
        .add_xaxis(list)
        .add_yaxis("商家1", list)
        .add_yaxis("商家2", list)
        .set_global_opts(title_opts=opts.TitleOpts(title="折线图-基本示例"))
        .render("line_test.html")
    )




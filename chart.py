import os
from pyecharts.charts import Bar, Line, EffectScatter
from pyecharts import options as opts
from pyecharts.faker import Faker

if __name__ == '__main__':

    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家1", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="这是主标题", subtitle="这是副标题"))
        .render("bar_base.html")
    )


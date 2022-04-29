#coding=utf-8
from pyecharts import GeoLines, Style
style = Style(
    title_top="#fff",
    title_pos = "center",
    width=1200,
    height=600,
    background_color="#C0C0C0"
)
style_geo = style.add(
    is_label_show=True,
    line_curve=0.2,
    line_opacity=0.6,
    legend_text_color="#eee",
    geo_normal_color="#404a59",
    legend_pos="right",
    geo_effect_period =12,
    geo_effect_symbol="roundRect",#动画形状
    geo_effect_symbolsize=10,#动画时间
    geo_effect_color="#aaa",
    label_color=['#FF0000', '#38B0DE', '#46bee9'],#动画颜色，一个接一个
    label_pos="right",
    label_formatter="{b}",
    label_text_color="#eee",
)
style_geo1 = style.add(
    is_label_show=True,
    line_curve=0.2,
    line_opacity=0.6,
    legend_text_color="#eee",
    geo_normal_color="#404a59",
    legend_pos="right",
    geo_effect_period =4,
    geo_effect_symbol="plane",
    geo_effect_symbolsize=10,
    label_color=['#FF0000', '#38B0DE', '#46bee9'],
    label_pos="right",
    label_formatter="{b}",
    label_text_color="#eee",
)


data_t = [
    ["武汉", "北京",2018.0413],
    ["乌鲁木齐", "伊宁",2018.0608],
    ["武汉", "南京",2018.0808],
    ["南京", "上海",2018.0810],
    ["武汉", "绵阳",2018.0911],
    ["武汉", "韶关",2018.1125],
    ["武汉", "郴州",2018.1212],
    ["武汉", "上海",2019.0107],
    ["武汉", "石家庄",2017.0625],
    ["武汉", "广州",2017.0922],
    ["武汉", "石家庄",2017.1025],
    ["石家庄", "青岛",2017.1028],
    ["武汉", "长沙",2017.1106],
    ["长沙", "湘潭",2017.1107],
    ["武汉", "天津",2017.1121],
    ["武汉", "北京",2019.0311],
    ["武汉", "厦门",2019.0320],
    ["武汉", "驻马店",2019.0404],
    ["武汉", "南京",2019.0523],
    ["武汉", "怀化",2019.0530],
    ["武汉", "吕梁",2019.0611],
    ["武汉", "广州",2019.0815],
    ["武汉", "广州",2019.0820],
    ["广州", "肇庆",2019.0822],
    ["肇庆", "宜昌",2019.0823],
    ["宜昌", "武汉",2019.0826],
]
data_p = [
    ["武汉", "保定",2018.0307],
    ["武汉", "乌鲁木齐",2018.0607],
    ["武汉", "海口",2018.0825],
    ["武汉", "成都",2018.1106],
    ["武汉", "青岛",2019.0411],
   
]
lines = GeoLines("mushui在UniStrong期间出差行程图", **style.init_style)
lines.add(
    "火车出行", data_t, tooltip_formatter="{a} : {c}", **style_geo
)
lines.add(
    "飞机出行", data_p, tooltip_formatter="{a} : {c}", **style_geo1
)
lines.render("mushui在UniStrong期间出差行程图.html")

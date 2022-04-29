# coding=GBK
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from pyecharts import Map, Geo, Page, Bar

db_connect = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='mushui1995',
    database='mushui',
    charset='GBK'
)
cur = db_connect.cursor()
engine = create_engine('mysql+pymysql://root:mushui1995@127.0.0.1:3306/mushui')  # 创建引擎
'''engine = create_engine('postgresql+psycopg2://' + pg_username + ':' + pg_password + '@' + pg_host + ':' + str(
    pg_port) + '/' + pg_database)'''

# sql_select_all="""SELECT * FROM 400_record"""
# cur.execute(sql_select_all)
# data_all=cur.fetchall()
data_all = pd.read_sql_table("400_record", engine,
                             columns=['日期', '时间', '渠道', '区域', '姓名', '联系方式', '处理人', '问题', '处理情况', '数量'])  # pandas读取SQL表格

'''以下为直接指令操作SQL方法'''
'''下面的为清洗处理人,清洗空值和含特殊符号值'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # 制作一个临时表格
cur.execute("""CREATE TABLE 400_temp1(处理人 varchar(20),数量 INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (处理人,数量) SELECT 处理人,数量 FROM 400_record""")  # 两者插入字段要一致
db_connect.commit()  # 似乎python操作MYSQL插入必须要这个
cur.execute("""DELETE FROM 400_temp1 WHERE  处理人  LIKE '%&%' or 处理人  LIKE '%，%' """)  # 舍去合作处理人
cur.execute("""DELETE FROM 400_temp1 WHERE 处理人 IS NULL""")  # 处理空值
cur.execute(
    """SELECT 处理人,SUM(数量) FROM 400_temp1 GROUP BY 处理人 ORDER BY SUM(数量) DESC""")  # order by 后加DESC为降序，不加为升序，如果是数字要SUM（）
data_person = cur.fetchall()
p_1 = []  # 处理人列表
p_2 = []  # 处理数量列表
for p in list(data_person):
    p_1.append(p[0])
    p_2.append(int(p[1]))

'''清洗渠道数据'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # 制作一个临时表格
cur.execute("""CREATE TABLE 400_temp1(渠道 varchar(20),数量 INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (渠道,数量) SELECT 渠道,数量 FROM 400_record""")  # 两者插入字段要一致
db_connect.commit()  # 似乎python操作MYSQL插入必须要这个
cur.execute("""UPDATE 400_temp1 SET 渠道="其他" WHERE 渠道="其它" """)
db_connect.commit()  # 似乎python操作MYSQL更新也必须要这个
cur.execute("""DELETE FROM 400_temp1 WHERE 渠道 IS NULL""")  # 处理空值
cur.execute(
    """SELECT 渠道,SUM(数量) FROM 400_temp1 GROUP BY 渠道 ORDER BY SUM(数量) DESC""")  # order by 后加DESC为降序，不加为升序，如果是数字要SUM（）
data_qudao = cur.fetchall()
qudao_1 = []  # 处理人列表
qudao_2 = []  # 处理数量列表
for qd in list(data_qudao):
    qudao_1.append(qd[0])
    qudao_2.append(int(qd[1]))

'''处理区域数据'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # 制作一个临时表格
cur.execute("""CREATE TABLE 400_temp1(渠道 varchar(20),区域 varchar(20),数量 INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (渠道,区域,数量) SELECT 渠道,区域,数量 FROM 400_record""")  # 两者插入字段要一致
db_connect.commit()  # 似乎python操作MYSQL插入必须要这个
cur.execute("""UPDATE 400_temp1 SET 渠道="其他" WHERE 渠道="其它" """)
db_connect.commit()  # 似乎python操作MYSQL更新也必须要这个
cur.execute("""UPDATE 400_temp1 SET 区域="四川" WHERE 区域="四川？" """)
db_connect.commit()  # 似乎python操作MYSQL更新也必须要这个
cur.execute("""UPDATE  400_temp1 SET 区域="内蒙古" WHERE 区域 LIKE "%内蒙古%" """)
db_connect.commit()
cur.execute("""UPDATE  400_temp1 SET 区域="江苏" WHERE 区域="南京" """)
db_connect.commit()  # 似乎python操作MYSQL更新也必须要这个
cur.execute("""DELETE FROM 400_temp1 WHERE 渠道 IS NULL""")  # 处理空值
cur.execute("""DELETE FROM 400_temp1 WHERE 区域="东北" """)  # 处理空值
cur.execute("""DELETE FROM 400_temp1 WHERE 区域 IS NULL""")  # 处理空值
cur.execute(
    """SELECT 区域,COUNT(区域) FROM 400_temp1 GROUP BY 区域 ORDER BY COUNT(区域) DESC""")  # order by 后加DESC为降序，不加为升序，如果是数字要SUM（）
data_quyu_done = cur.fetchall()
quyu_1 = []
quyu_2 = []
for qy in list(data_quyu_done):
    quyu_1.append(qy[0])
    quyu_2.append(int(qy[1]))

'''测量数据'''
cur.execute("""SELECT 区域,COUNT(区域) FROM 400_temp1 WHERE 渠道="测量" GROUP BY 区域 ORDER BY COUNT(区域) DESC""")
data_quyu_survey_done = cur.fetchall()
quyu_s1 = []
quyu_s2 = []
for qys in list(data_quyu_survey_done):
    quyu_s1.append(qys[0])
    quyu_s2.append(int(qys[1]))

'''集思数据'''
cur.execute("""SELECT 区域,COUNT(区域) FROM 400_temp1 WHERE 渠道="集思" GROUP BY 区域 ORDER BY COUNT(区域) DESC""")
data_quyu_gis_done = cur.fetchall()
quyu_g1 = []
quyu_g2 = []
for qyg in list(data_quyu_gis_done):
    quyu_g1.append(qyg[0])
    quyu_g2.append(int(qyg[1]))

'''日期时间等处理'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # 制作一个临时表格
cur.execute("""CREATE TABLE 400_temp1(日期 date,渠道 varchar(20),数量 INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (日期,渠道,数量) SELECT 日期,渠道,数量 FROM 400_record""")  # 两者插入字段要一致

cur.execute(
    """SELECT DATE_FORMAT(日期,'%y%m') AS 年月,COUNT(DATE_FORMAT(日期,'%y%m')) AS 年月统计 FROM 400_temp1  GROUP BY 年月 ORDER BY 
    年月""")  # 按月份接电话数量
date_all = cur.fetchall()
date_index = []
date_data = []
for date in date_all:
    date_index.append(date[0])
    date_data.append(date[1])

'''日期测量数据'''
cur.execute(
    """SELECT DATE_FORMAT(日期,'%y%m') AS 年月,COUNT(DATE_FORMAT(日期,'%y%m')) AS 年月统计 FROM 400_temp1 WHERE 渠道="测量"  GROUP 
    BY 年月 ORDER BY 年月""")
date_survey = cur.fetchall()
date_s1 = []
date_s2 = []
for date_s in date_survey:
    date_s1.append(date_s[0])
    date_s2.append(date_s[1])

'''日期集思数据'''
cur.execute(
    """SELECT DATE_FORMAT(日期,'%y%m') AS 年月,COUNT(DATE_FORMAT(日期,'%y%m')) AS 年月统计 FROM 400_temp1 WHERE 渠道="集思"  GROUP 
    BY 年月 ORDER BY 年月""")
date_gis = cur.fetchall()
date_g1 = []
date_g2 = []
for date_g in date_gis:
    date_g1.append(date_g[0])
    date_g2.append(date_g[1])

'''以下为使用pandas的读表法'''
# data_b=data_all.groupby(['渠道'])['数量'].count().sort_values(ascending=False)#降序，True为正序
data_c = data_all.groupby(['区域', '渠道'])['数量'].count()
data_quyu = data_all.groupby(['区域'])['数量'].count().sort_values(ascending=False)
data_map = data_all.groupby(["区域"])['数量'].count()
'''注意以下部分append不能直接print，其没有返回值
aa=[]#data_c=data_all.groupby(['区域','渠道'])['数量'].count()的索引
a_add=[]#索引+数值
for i in range(0,len(data_c)):
    aa=list(data_c.index[i])
    aa.append(data_c[i])
    a_add.append(aa)
    aa=[]
print(a_add)'''

count1 = 0
sql_select_buy = """SELECT 问题 FROM 400_record WHERE 问题 LIKE '%购%' or 问题 LIKE '%买%' or  问题 LIKE '%询%' or  问题 LIKE '%价%' """  # 有购买意向的人员统计

cur.execute(sql_select_buy)
result_select_buy = cur.fetchall()
# print(type(result_select_buy))
page = Page()
bar1 = Bar("合众思壮400电话统计分析，自201707起", "按处理人统计")
bar1.add("接听数量", p_1, p_2, xaxis_rotate=60, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(p_2),
         is_label_show=True, is_datazoom_show=True)  # data_p.index是索引，不然只有数值，索引做x轴
page.add(bar1)

bar2 = Bar("", "按渠道统计")
# bar2.add("接听数量",list(data_b.index),list(data_b),xaxis_rotate=0,mark_line=["average"],yaxis_min=0,yaxis_max=np.max(list(data_b)),is_label_show=True)#pandas方法：data_p.index是索引，不然只有数值，索引做x轴
bar2.add("接听数量", qudao_1, qudao_2, xaxis_rotate=0, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(qudao_2),
         is_label_show=True)
page.add(bar2)

bar_quyu = Bar("", "按区域统计:清洗后")
bar_quyu.add("接听数量", quyu_1, quyu_2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(quyu_2),
             is_label_show=True, is_datazoom_show=True)
page.add(bar_quyu)

bar3 = Bar("", "按区域统计:未清洗")
bar3.add("接听数量", list(data_quyu.index), list(data_quyu), xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
         yaxis_max=np.max(list(data_quyu)), is_label_show=True, is_datazoom_show=True)
page.add(bar3)

bar_date = Bar("", "按月份统计:全部")
bar_date.add("接听数量", date_index, date_data, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
             yaxis_max=np.max(date_data), is_label_show=True)
page.add(bar_date)

bar_date_survey = Bar("", "按月份统计分渠道")
bar_date_survey.add("测量接听数量", date_s1, date_s2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
                    yaxis_max=np.max(date_s2), is_label_show=True, is_datazoom_show=True)
bar_date_survey.add("集思接听数量", date_s1, date_g2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
                    yaxis_max=np.max(date_g2), is_label_show=True, is_datazoom_show=True)
page.add(bar_date_survey)

map_all = Map("UniStrong400电话全国分布图", width=1000, height=800)
map_all.add("UniStrong400电话全国分布图", list(data_map.index), list(data_map), maptype='china', is_visualmap=True,
            visual_range=[min(list(data_map)), max(list(data_map))], visual_text_color='#000', is_label_show=True)
page.add(map_all)

map_survey = Map("UniStrong400电话全国分布图(测量)", width=1000, height=800)
map_survey.add("UniStrong400电话全国分布图(测量)", quyu_s1, quyu_s2, maptype='china', is_visualmap=True,
               visual_range=[min(quyu_s2), max(quyu_s2)], visual_text_color='#000', is_label_show=True)
page.add(map_survey)

map_gis = Map("UniStrong400电话全国分布图(GIS)", width=1000, height=800)
map_gis.add("UniStrong400电话全国分布图(GIS)", quyu_g1, quyu_g2, maptype='china', is_visualmap=True,
            visual_range=[min(quyu_g2), max(quyu_g2)], visual_text_color='#000', is_label_show=True)
page.add(map_gis)

page.render("合众思壮400电话统计分析，自201707起.html")

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
engine = create_engine('mysql+pymysql://root:mushui1995@127.0.0.1:3306/mushui')  # ��������
'''engine = create_engine('postgresql+psycopg2://' + pg_username + ':' + pg_password + '@' + pg_host + ':' + str(
    pg_port) + '/' + pg_database)'''

# sql_select_all="""SELECT * FROM 400_record"""
# cur.execute(sql_select_all)
# data_all=cur.fetchall()
data_all = pd.read_sql_table("400_record", engine,
                             columns=['����', 'ʱ��', '����', '����', '����', '��ϵ��ʽ', '������', '����', '�������', '����'])  # pandas��ȡSQL���

'''����Ϊֱ��ָ�����SQL����'''
'''�����Ϊ��ϴ������,��ϴ��ֵ�ͺ��������ֵ'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # ����һ����ʱ���
cur.execute("""CREATE TABLE 400_temp1(������ varchar(20),���� INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (������,����) SELECT ������,���� FROM 400_record""")  # ���߲����ֶ�Ҫһ��
db_connect.commit()  # �ƺ�python����MYSQL�������Ҫ���
cur.execute("""DELETE FROM 400_temp1 WHERE  ������  LIKE '%&%' or ������  LIKE '%��%' """)  # ��ȥ����������
cur.execute("""DELETE FROM 400_temp1 WHERE ������ IS NULL""")  # �����ֵ
cur.execute(
    """SELECT ������,SUM(����) FROM 400_temp1 GROUP BY ������ ORDER BY SUM(����) DESC""")  # order by ���DESCΪ���򣬲���Ϊ�������������ҪSUM����
data_person = cur.fetchall()
p_1 = []  # �������б�
p_2 = []  # ���������б�
for p in list(data_person):
    p_1.append(p[0])
    p_2.append(int(p[1]))

'''��ϴ��������'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # ����һ����ʱ���
cur.execute("""CREATE TABLE 400_temp1(���� varchar(20),���� INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (����,����) SELECT ����,���� FROM 400_record""")  # ���߲����ֶ�Ҫһ��
db_connect.commit()  # �ƺ�python����MYSQL�������Ҫ���
cur.execute("""UPDATE 400_temp1 SET ����="����" WHERE ����="����" """)
db_connect.commit()  # �ƺ�python����MYSQL����Ҳ����Ҫ���
cur.execute("""DELETE FROM 400_temp1 WHERE ���� IS NULL""")  # �����ֵ
cur.execute(
    """SELECT ����,SUM(����) FROM 400_temp1 GROUP BY ���� ORDER BY SUM(����) DESC""")  # order by ���DESCΪ���򣬲���Ϊ�������������ҪSUM����
data_qudao = cur.fetchall()
qudao_1 = []  # �������б�
qudao_2 = []  # ���������б�
for qd in list(data_qudao):
    qudao_1.append(qd[0])
    qudao_2.append(int(qd[1]))

'''������������'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # ����һ����ʱ���
cur.execute("""CREATE TABLE 400_temp1(���� varchar(20),���� varchar(20),���� INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (����,����,����) SELECT ����,����,���� FROM 400_record""")  # ���߲����ֶ�Ҫһ��
db_connect.commit()  # �ƺ�python����MYSQL�������Ҫ���
cur.execute("""UPDATE 400_temp1 SET ����="����" WHERE ����="����" """)
db_connect.commit()  # �ƺ�python����MYSQL����Ҳ����Ҫ���
cur.execute("""UPDATE 400_temp1 SET ����="�Ĵ�" WHERE ����="�Ĵ���" """)
db_connect.commit()  # �ƺ�python����MYSQL����Ҳ����Ҫ���
cur.execute("""UPDATE  400_temp1 SET ����="���ɹ�" WHERE ���� LIKE "%���ɹ�%" """)
db_connect.commit()
cur.execute("""UPDATE  400_temp1 SET ����="����" WHERE ����="�Ͼ�" """)
db_connect.commit()  # �ƺ�python����MYSQL����Ҳ����Ҫ���
cur.execute("""DELETE FROM 400_temp1 WHERE ���� IS NULL""")  # �����ֵ
cur.execute("""DELETE FROM 400_temp1 WHERE ����="����" """)  # �����ֵ
cur.execute("""DELETE FROM 400_temp1 WHERE ���� IS NULL""")  # �����ֵ
cur.execute(
    """SELECT ����,COUNT(����) FROM 400_temp1 GROUP BY ���� ORDER BY COUNT(����) DESC""")  # order by ���DESCΪ���򣬲���Ϊ�������������ҪSUM����
data_quyu_done = cur.fetchall()
quyu_1 = []
quyu_2 = []
for qy in list(data_quyu_done):
    quyu_1.append(qy[0])
    quyu_2.append(int(qy[1]))

'''��������'''
cur.execute("""SELECT ����,COUNT(����) FROM 400_temp1 WHERE ����="����" GROUP BY ���� ORDER BY COUNT(����) DESC""")
data_quyu_survey_done = cur.fetchall()
quyu_s1 = []
quyu_s2 = []
for qys in list(data_quyu_survey_done):
    quyu_s1.append(qys[0])
    quyu_s2.append(int(qys[1]))

'''��˼����'''
cur.execute("""SELECT ����,COUNT(����) FROM 400_temp1 WHERE ����="��˼" GROUP BY ���� ORDER BY COUNT(����) DESC""")
data_quyu_gis_done = cur.fetchall()
quyu_g1 = []
quyu_g2 = []
for qyg in list(data_quyu_gis_done):
    quyu_g1.append(qyg[0])
    quyu_g2.append(int(qyg[1]))

'''����ʱ��ȴ���'''
cur.execute("""DROP TABLE IF EXISTS 400_temp1""")  # ����һ����ʱ���
cur.execute("""CREATE TABLE 400_temp1(���� date,���� varchar(20),���� INT(11))""")
cur.execute("""INSERT INTO 400_temp1 (����,����,����) SELECT ����,����,���� FROM 400_record""")  # ���߲����ֶ�Ҫһ��

cur.execute(
    """SELECT DATE_FORMAT(����,'%y%m') AS ����,COUNT(DATE_FORMAT(����,'%y%m')) AS ����ͳ�� FROM 400_temp1  GROUP BY ���� ORDER BY 
    ����""")  # ���·ݽӵ绰����
date_all = cur.fetchall()
date_index = []
date_data = []
for date in date_all:
    date_index.append(date[0])
    date_data.append(date[1])

'''���ڲ�������'''
cur.execute(
    """SELECT DATE_FORMAT(����,'%y%m') AS ����,COUNT(DATE_FORMAT(����,'%y%m')) AS ����ͳ�� FROM 400_temp1 WHERE ����="����"  GROUP 
    BY ���� ORDER BY ����""")
date_survey = cur.fetchall()
date_s1 = []
date_s2 = []
for date_s in date_survey:
    date_s1.append(date_s[0])
    date_s2.append(date_s[1])

'''���ڼ�˼����'''
cur.execute(
    """SELECT DATE_FORMAT(����,'%y%m') AS ����,COUNT(DATE_FORMAT(����,'%y%m')) AS ����ͳ�� FROM 400_temp1 WHERE ����="��˼"  GROUP 
    BY ���� ORDER BY ����""")
date_gis = cur.fetchall()
date_g1 = []
date_g2 = []
for date_g in date_gis:
    date_g1.append(date_g[0])
    date_g2.append(date_g[1])

'''����Ϊʹ��pandas�Ķ���'''
# data_b=data_all.groupby(['����'])['����'].count().sort_values(ascending=False)#����TrueΪ����
data_c = data_all.groupby(['����', '����'])['����'].count()
data_quyu = data_all.groupby(['����'])['����'].count().sort_values(ascending=False)
data_map = data_all.groupby(["����"])['����'].count()
'''ע�����²���append����ֱ��print����û�з���ֵ
aa=[]#data_c=data_all.groupby(['����','����'])['����'].count()������
a_add=[]#����+��ֵ
for i in range(0,len(data_c)):
    aa=list(data_c.index[i])
    aa.append(data_c[i])
    a_add.append(aa)
    aa=[]
print(a_add)'''

count1 = 0
sql_select_buy = """SELECT ���� FROM 400_record WHERE ���� LIKE '%��%' or ���� LIKE '%��%' or  ���� LIKE '%ѯ%' or  ���� LIKE '%��%' """  # �й����������Աͳ��

cur.execute(sql_select_buy)
result_select_buy = cur.fetchall()
# print(type(result_select_buy))
page = Page()
bar1 = Bar("����˼׳400�绰ͳ�Ʒ�������201707��", "��������ͳ��")
bar1.add("��������", p_1, p_2, xaxis_rotate=60, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(p_2),
         is_label_show=True, is_datazoom_show=True)  # data_p.index����������Ȼֻ����ֵ��������x��
page.add(bar1)

bar2 = Bar("", "������ͳ��")
# bar2.add("��������",list(data_b.index),list(data_b),xaxis_rotate=0,mark_line=["average"],yaxis_min=0,yaxis_max=np.max(list(data_b)),is_label_show=True)#pandas������data_p.index����������Ȼֻ����ֵ��������x��
bar2.add("��������", qudao_1, qudao_2, xaxis_rotate=0, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(qudao_2),
         is_label_show=True)
page.add(bar2)

bar_quyu = Bar("", "������ͳ��:��ϴ��")
bar_quyu.add("��������", quyu_1, quyu_2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0, yaxis_max=np.max(quyu_2),
             is_label_show=True, is_datazoom_show=True)
page.add(bar_quyu)

bar3 = Bar("", "������ͳ��:δ��ϴ")
bar3.add("��������", list(data_quyu.index), list(data_quyu), xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
         yaxis_max=np.max(list(data_quyu)), is_label_show=True, is_datazoom_show=True)
page.add(bar3)

bar_date = Bar("", "���·�ͳ��:ȫ��")
bar_date.add("��������", date_index, date_data, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
             yaxis_max=np.max(date_data), is_label_show=True)
page.add(bar_date)

bar_date_survey = Bar("", "���·�ͳ�Ʒ�����")
bar_date_survey.add("������������", date_s1, date_s2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
                    yaxis_max=np.max(date_s2), is_label_show=True, is_datazoom_show=True)
bar_date_survey.add("��˼��������", date_s1, date_g2, xaxis_rotate=80, mark_line=["average"], yaxis_min=0,
                    yaxis_max=np.max(date_g2), is_label_show=True, is_datazoom_show=True)
page.add(bar_date_survey)

map_all = Map("UniStrong400�绰ȫ���ֲ�ͼ", width=1000, height=800)
map_all.add("UniStrong400�绰ȫ���ֲ�ͼ", list(data_map.index), list(data_map), maptype='china', is_visualmap=True,
            visual_range=[min(list(data_map)), max(list(data_map))], visual_text_color='#000', is_label_show=True)
page.add(map_all)

map_survey = Map("UniStrong400�绰ȫ���ֲ�ͼ(����)", width=1000, height=800)
map_survey.add("UniStrong400�绰ȫ���ֲ�ͼ(����)", quyu_s1, quyu_s2, maptype='china', is_visualmap=True,
               visual_range=[min(quyu_s2), max(quyu_s2)], visual_text_color='#000', is_label_show=True)
page.add(map_survey)

map_gis = Map("UniStrong400�绰ȫ���ֲ�ͼ(GIS)", width=1000, height=800)
map_gis.add("UniStrong400�绰ȫ���ֲ�ͼ(GIS)", quyu_g1, quyu_g2, maptype='china', is_visualmap=True,
            visual_range=[min(quyu_g2), max(quyu_g2)], visual_text_color='#000', is_label_show=True)
page.add(map_gis)

page.render("����˼׳400�绰ͳ�Ʒ�������201707��.html")

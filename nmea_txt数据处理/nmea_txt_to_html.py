#coding=UTF-8
#说明：使用情景：至少y有GPGGA,GPGST语句,且要有固定解，数据不能过少,使用txt格式数据最好,仅适用于中国精度的收敛测试情况
from pyecharts import Line
from pyecharts import Liquid
from pyecharts import Scatter
from pyecharts import Pie
from pyecharts import Grid
from pyecharts import EffectScatter
from pyecharts import Gauge
from pyecharts import Page
import pandas as pd
import csv
import os
import math
import numpy as np

path1="C:\\Users\\mushui\\Desktop\\test1"
#path2="C:\\Users\\mushui\\Desktop\\newpng\\千寻\\5KM\\房屋遮挡"
filelist = os.listdir(path1)
for files in filelist:
 #Olddir = os.path.join(path1,files)
  filename = os.path.splitext(files)[0]#文件名
  filetype = os.path.splitext(files)[1]#文件后缀
  def LatLon2X(latitude, longitude):
	  a = 6378137.0
	  # b = 6356752.3142
	  # c = 6399593.6258
	  alpha = 1 / 298.257223563
	  e2 = 0.00669437999013
		# epep = 0.00673949674227


		#将经纬度转换为弧度
	  latitude2Rad = (math.pi / 180.0) * latitude

	  beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
	  L = beltNo * 3 #计算中央经线
	  l0 = longitude - L #经差
	  tsin = math.sin(latitude2Rad)
	  tcos = math.cos(latitude2Rad)
	  t = math.tan(latitude2Rad)
	  m = (math.pi / 180.0) * l0 * tcos
	  et2 = e2 * pow(tcos, 2)
	  et3 = e2 * pow(tsin, 2)
	  X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
			4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
	  N = a / math.sqrt(1 - et3)

	  x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
		61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
	  return x	
  def LatLon2Y(latitude, longitude):
	  a = 6378137.0
		# b = 6356752.3142
		# c = 6399593.6258
	  alpha = 1 / 298.257223563
	  e2 = 0.00669437999013
		# epep = 0.00673949674227


		#将经纬度转换为弧度
	  latitude2Rad = (math.pi / 180.0) * latitude

	  beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
	  L = beltNo * 3 #计算中央经线
	  l0 = longitude - L #经差
	  tsin = math.sin(latitude2Rad)
	  tcos = math.cos(latitude2Rad)
	  t = math.tan(latitude2Rad)
	  m = (math.pi / 180.0) * l0 * tcos
	  et2 = e2 * pow(tcos, 2)
	  et3 = e2 * pow(tsin, 2)
	  X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
			4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
	  N = a / math.sqrt(1 - et3)
	  y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
		5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)
	  return y 
  def pingjunzhi(list1):
	  sum1 = 0.0
	  for item in list1:
		  sum1 += item
	  return sum1/len(list1)
   #求二维中误差
  def EWZWC(list1,list2):
	  sum1=0.0
	  for i in range(0,(len(list1)-1)):
		  sum1=sum1+(list1[i]-pingjunzhi(list1))**2+(list2[i]-pingjunzhi(list2))**2
		  ave=np.sqrt(float(sum1/len(list1)))
	  return ave
 
  x_datas=[]#北坐标
  y_datas=[]#东坐标
  h_datas=[]#高程
  x_datas1=[]#北坐标
  y_datas1=[]#东坐标
  h_datas1=[]#高程
  x_datas2=[]#北坐标
  y_datas2=[]#东坐标
  h_datas2=[]#高程
  x_datas4=[]#北坐标
  y_datas4=[]#东坐标
  h_datas4=[]#高程
  x_datas5=[]#北坐标
  y_datas5=[]#东坐标
  h_datas5=[]#高程
  pt=[]
  ptfixed=[]
  pt1=[]#点
  pt2=[]
  pt4=[]
  pt5=[]
  sat_used=[]#解算卫星
  sat_all=[]#搜索卫星
  Hrms=[]
  Vrms=[]
  Hrms1=[]
  Vrms1=[]
  Hrms2=[]
  Vrms2=[]
  Hrms4=[]
  Vrms4=[]
  Hrms5=[]
  Vrms5=[]
  sumhv=0
  sum1=0
  sum2=0
  sum5=0
  sum4=0
  sum123=0
  Hai=[]#海拔高
  pt=[]
  #det=[]#大地水准面差距
  x_datas=[]#投影北坐标
  y_datas=[]#投影东坐标
  h_datas=[]#大地高
  utc1=0
  utc2=0
  utc4=0
  utc5=0
  utcgst=0
  file1=open(path1+'\\'+files)
  for line in file1.readlines():
	  linenum=line.strip().split(",")
	  if(linenum[0]=="$GPGGA" and linenum[6]=="4"):
		  sum123=sum123+1
		  pt.append(int(sum123))
		  sum4=sum4+1
		  if(sum4==1):
			  firstfixed=sum123-1
		  lon_du=math.floor(float(linenum[2])/100)+(float(linenum[2])%100)/60
		  lat_du=math.floor(float(linenum[4])/100)+(float(linenum[4])%100)/60
		  x_datas.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas.append(round(float(linenum[9])+float(linenum[11]),3))
		  utc4=linenum[1]
		  
		  pt4.append(int(sum123))
		  ptfixed.append(sum4)
		  x_datas4.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas4.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas4.append(round(float(linenum[9])+float(linenum[11]),3))
		  
	  elif(linenum[0]=="$GPGGA" and linenum[6]=="1"):
		  sum123=sum123+1
		  pt.append(int(sum123))
		  sum1=sum1+1
		  
		  lon_du=math.floor(float(linenum[2])/100)+(float(linenum[2])%100)/60
		  lat_du=math.floor(float(linenum[4])/100)+(float(linenum[4])%100)/60
		  x_datas.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas.append(round(float(linenum[9])+float(linenum[11]),3))
		  utc1=linenum[1]
		  
		  pt1.append(int(sum123))
		  x_datas1.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas1.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas1.append(round(float(linenum[9])+float(linenum[11]),3))
	  elif(linenum[0]=="$GPGGA" and linenum[6]=="2"):
		  sum123=sum123+1
		  pt.append(int(sum123))
		  sum2=sum2+1
		  
		  lon_du=math.floor(float(linenum[2])/100)+(float(linenum[2])%100)/60
		  lat_du=math.floor(float(linenum[4])/100)+(float(linenum[4])%100)/60
		  x_datas.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas.append(round(float(linenum[9])+float(linenum[11]),3))
		  utc2=linenum[1]
		  
		  pt2.append(int(sum123))
		  x_datas2.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas2.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas2.append(round(float(linenum[9])+float(linenum[11]),3))
	  elif(linenum[0]=="$GPGGA" and linenum[6]=="5"):
		  sum123=sum123+1
		  pt.append(int(sum123))
		  sum5=sum5+1
		  
		  lon_du=math.floor(float(linenum[2])/100)+(float(linenum[2])%100)/60
		  lat_du=math.floor(float(linenum[4])/100)+(float(linenum[4])%100)/60
		  x_datas.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas.append(round(float(linenum[9])+float(linenum[11]),3))
		  utc5=linenum[1]
		  
		  pt5.append(int(sum123))
		  x_datas5.append(round(LatLon2X(lon_du,lat_du),3))
		  y_datas5.append(round(LatLon2Y(lon_du,lat_du),3))
		  h_datas5.append(round(float(linenum[9])+float(linenum[11]),3))
	  
	  elif(linenum[0]=="$GPGST" or linenum[0]=="$GNGST"):
		  utcgst=linenum[1]
		  Hrms.append(round(np.sqrt(float(linenum[6])**2+float(linenum[7])**2),3))
		  str=linenum[8]
		  Vrms.append(float(str[:-3]))
		  if(utcgst==utc4):
			  Hrms4.append(round(np.sqrt(float(linenum[6])**2+float(linenum[7])**2),3))
			  str=linenum[8]
			  Vrms4.append(float(str[:-3]))
		  elif(utcgst==utc1):
			  Hrms1.append(round(np.sqrt(float(linenum[6])**2+float(linenum[7])**2),3))
			  str=linenum[8]
			  Vrms1.append(float(str[:-3]))
		  elif(utcgst==utc2):
			  Hrms2.append(round(np.sqrt(float(linenum[6])**2+float(linenum[7])**2),3))
			  str=linenum[8]
			  Vrms2.append(float(str[:-3]))
		  elif(utcgst==utc5):
			  Hrms5.append(round(np.sqrt(float(linenum[6])**2+float(linenum[7])**2),3))
			  str=linenum[8]
			  Vrms5.append(float(str[:-3]))
  #高斯正算,WGS84椭球,3度带

  page=Page()
  
  es1 =Scatter("北坐标变化图",width=1200)
  es1.add("SINGLE",pt1,x_datas1,symbol_size=3, yaxis_min=np.min(x_datas),yaxis_max= np.max(x_datas))  
  es1.add("DGNSS", pt2,x_datas2,symbol_size=3, yaxis_min=np.min(x_datas),yaxis_max= np.max(x_datas))
  es1.add("FLOAT", pt5,x_datas5,symbol_size=3, yaxis_min=np.min(x_datas),yaxis_max= np.max(x_datas)) 
  es1.add("FIXED", pt4,x_datas4,symbol_size=3, yaxis_min=np.min(x_datas),yaxis_max= np.max(x_datas))
  page.add(es1)
  es2 =Scatter("东坐标变化图",width=1200)
  es2.add("SINGLE", pt1,y_datas1, symbol_size=3, yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))  
  es2.add("DGNSS", pt2,y_datas2, symbol_size=3, yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))
  es2.add("FLOAT", pt5,y_datas5, symbol_size=3, yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas)) 
  es2.add("FIXED", pt4,y_datas4,symbol_size=3,  yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))
  page.add(es2)
  es3 =Scatter("高程变化图",width=1200)
  es3.add("SINGLE", pt1,h_datas1,symbol_size=3,  yaxis_min=np.min(h_datas),yaxis_max= np.max(h_datas))  
  es3.add("DGNSS", pt2,h_datas2, symbol_size=3, yaxis_min=np.min(h_datas),yaxis_max= np.max(h_datas))
  es3.add("FLOAT", pt5,h_datas5, symbol_size=3, yaxis_min=np.min(h_datas),yaxis_max= np.max(h_datas)) 
  es3.add("FIXED", pt4,h_datas4, symbol_size=3, yaxis_min=np.min(h_datas),yaxis_max= np.max(h_datas))
  page.add(es3)
  if(utcgst==0):
	  es4 =Scatter("没有GST数据！不能反馈误差偏差图！")
	  page.add(es4)
  elif(utcgst!=0):
	  if(sum4==0):
		  es4 =Scatter("Hrms变化图",width=1200)
		  es4.add("SINGLE", pt1,Hrms1, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))  
		  es4.add("DGNSS", pt2,Hrms2, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))
		  es4.add("FLOAT", pt5,Hrms5, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms)) 
		  es4.add("FIXED", pt4,Hrms4, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))
		  page.add(es4)
	  elif(sum4!=0):
		  es4 =Scatter("Hrms变化图\n收敛到固定解的时间为：%r分钟"%math.floor(firstfixed/60)+"%r秒"%(firstfixed%60)+"(即%r秒)"%firstfixed,width=1200)
		  es4.add("SINGLE", pt1,Hrms1, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))  
		  es4.add("DGNSS", pt2,Hrms2, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))
		  es4.add("FLOAT", pt5,Hrms5, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms)) 
		  es4.add("FIXED", pt4,Hrms4, symbol_size=3, yaxis_min=np.min(Hrms),yaxis_max= np.max(Hrms))
		  page.add(es4)	
	  es5 =Scatter("Vrms变化图",width=1200)
	  es5.add("SINGLE", pt1,Vrms1, symbol_size=3, yaxis_min=np.min(Vrms),yaxis_max= np.max(Vrms))  
	  es5.add("DGNSS", pt2,Vrms2, symbol_size=3, yaxis_min=np.min(Vrms),yaxis_max= np.max(Vrms))
	  es5.add("FLOAT", pt5,Vrms5, symbol_size=3, yaxis_min=np.min(Vrms),yaxis_max= np.max(Vrms)) 
	  es5.add("FIXED", pt4,Vrms4, symbol_size=3, yaxis_min=np.min(Vrms),yaxis_max= np.max(Vrms))
	  page.add(es5)
  es6 =Scatter("点位分布图")
  es6.add("SINGLE", x_datas1, y_datas1,symbol_size=5, xaxis_min=np.min(x_datas),xaxis_max= np.max(x_datas),yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))  
  es6.add("DGNSS", x_datas2, y_datas2,symbol_size=5, xaxis_min=np.min(x_datas),xaxis_max= np.max(x_datas),yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))
  es6.add("FLOAT", x_datas5, y_datas5,symbol_size=5, xaxis_min=np.min(x_datas),xaxis_max= np.max(x_datas),yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas)) 
  es6.add("FIXED",x_datas4, y_datas4,symbol_size=5, xaxis_min=np.min(x_datas),xaxis_max= np.max(x_datas),yaxis_min=np.min(y_datas),yaxis_max= np.max(y_datas))
  page.add(es6)
  if(sum4==0):
	  gauge = Gauge("固定率")
	  gauge.add("固定率图", "固定率", round(100*sum4/sum123,3))
	  page.add(gauge)
  elif(sum4!=0):
	  rarr=EWZWC(x_datas4,y_datas4)
	  line1=Line("固定解北坐标变化图",width=1200)    
	  line1.add("北坐标",ptfixed,x_datas4,yaxis_min=np.min(x_datas4),yaxis_max= np.max(x_datas4),mark_point=["max","min"],mark_line=["average"]) 
	  page.add(line1)
	  line2=Line("固定解东坐标变化图",width=1200)  
	  line2.add("东坐标",ptfixed,y_datas4,yaxis_min=np.min(y_datas4),yaxis_max= np.max(y_datas4),mark_point=["max","min"],mark_line=["average"]) 
	  page.add(line2)
	  line3=Line("固定解高程变化图",width=1200)  
	  line3.add("高程",ptfixed,h_datas4,yaxis_min=np.min(h_datas4),yaxis_max= np.max(h_datas4),mark_point=["max","min"],mark_line=["average"]) 
	  page.add(line3)
	  es =Scatter("固定解点位分布图\n固定解σ=%r米"%round(rarr,3))
	  es.add("点", x_datas4, y_datas4,symbol_size=6,  xaxis_min=np.min(x_datas4),xaxis_max= np.max(x_datas4),yaxis_min=np.min(y_datas4),yaxis_max= np.max(y_datas4))
	  page.add(es)
	  gauge = Gauge("固定率")
	  gauge.add("固定率图", "固定率", round(100*sum4/sum123,3))
	  page.add(gauge)  
 

  '''#高斯反算
	def XY2LatLon(X, Y, L0):

		iPI = 0.0174532925199433
		a = 6378137.0
		f= 0.00335281006247
		ZoneWide = 3 #按3度带进行投影

		ProjNo = int(X / 1000000)
		L0 = L0 * iPI
		X0 = ProjNo * 1000000 + 500000
		Y0 = 0
		xval = X - X0
		yval = Y - Y0

		e2 = 2 * f - f * f #第一偏心率平方
		e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
		ee = e2 / (1 - e2) #第二偏心率平方

		M = yval
		u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

		fai = u \
			  + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
			  + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
			  + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
			  + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
		C = ee * math.cos(fai) * math.cos(fai)
		T = math.tan(fai) * math.tan(fai)
		NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
		R = a * (1 - e2) / math.sqrt(
			(1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
		D = xval / NN

		#计算经纬度（弧度单位的经纬度）
		longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
		5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
		latitude1 = fai - (NN * math.tan(fai) / R) * (
		D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
		61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)

		#换换为deg
		longitude = longitude1 / iPI
		latitude = latitude1 / iPI

		return latitude, longitude'''
  page.render("C:\\Users\\mushui\\Desktop\\test2\\%s.html"%filename)
  
print('over!')

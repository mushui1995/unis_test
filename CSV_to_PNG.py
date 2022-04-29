#coding=GBK
import matplotlib.pyplot as plt
import csv
from pylab import *
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker
plt.rcParams['font.sans-serif']=['simhei'] #解决中文显示
plt.rcParams['axes.unicode_minus'] = False
path1="C:\\Users\\mushui\\Desktop\\test2"
#path2="C:\\Users\\mushui\\Desktop\\newpng\\千寻\\5KM\\房屋遮挡"
filelist = os.listdir(path1)
for files in filelist:
 #Olddir = os.path.join(path1,files)
  filename = os.path.splitext(files)[0]#文件名
  filetype = os.path.splitext(files)[1]#文件后缀
  
  with open(os.path.join(path1,files) ) as f:#打开这个文件，并将结果文件对象存储在f中 

   reader=csv.reader(f)#创建一个阅读器reader  
   #header_row=next(reader)
   x_datas=[]
   y_datas=[]
   for row in reader:
	   x_data=float(row[2])
	   x_datas.append(x_data)
	   y_data=float(row[3])
	   y_datas.append(y_data)
	
   #print(x_datas)
    
    #求平均值
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
    #圈出范围圆
  #def circle(x,y,r,count=2000):
  x=pingjunzhi(x_datas)
  y=pingjunzhi(y_datas)
  #1倍
  xarr=[]
  yarr=[]
  rarr=EWZWC(x_datas,y_datas)
  for i1 in range(1,2000):
	  j = float(i1)/2000 * 2 * np.pi
	  xarr.append(x+rarr*np.cos(j))
	  yarr.append(y+rarr*np.sin(j))
  l1,=plt.plot(xarr,yarr,'g.',linewidth=0.1,alpha=0.3)
  #l1=plt.scatter(xarr,yarr,marker = '.', color = 'blue', s = 1,alpha=0.8)
  
  #2倍
  xbrr=[]
  ybrr=[]
  rbrr=2*EWZWC(x_datas,y_datas)
  for i2 in range(1,2000):
	  j2 = float(i2)/2000 * 2 * np.pi
	  xbrr.append(x+rbrr*np.cos(j2))
	  ybrr.append(y+rbrr*np.sin(j2))
  l2,=plt.plot(xbrr,ybrr,'b.',linewidth=0.1,alpha=0.2)
  #l2=plt.scatter(xbrr,ybrr,marker = '.', color = 'blue', s = 1,alpha=0.5)
  #3倍
  xcrr=[]
  ycrr=[]
  rcrr=3*EWZWC(x_datas,y_datas)
  for i3 in range(1,2000):
	  j3 = float(i3)/2000 * 2 * np.pi
	  xcrr.append(x+rcrr*np.cos(j3))
	  ycrr.append(y+rcrr*np.sin(j3))
  l3,=plt.plot(xcrr,ycrr,'y.',linewidth=0.1,alpha=0.1)
  #l3=plt.scatter(xcrr,ycrr,marker = '.', color = 'blue', s = 1,alpha=0.3)
 
  l1.set_label("σ=%r米"%round(rarr,3)) 
  l2.set_label("2σ=%r米"%round(rbrr,3)) 
  l3.set_label("3σ=%r米"%round(rcrr,3)) 
 
  plt.plot(x_datas, y_datas, 'r.',linewidth=1,alpha=0.5)
  plt.title(u"%s"%filename)
  plt.legend(["σ=%r米"%round(rarr,3),"2σ=%r米"%round(rbrr,3),"3σ=%r米"%round(rcrr,3)],loc=1) 
  plt.xlabel(u"北坐标")
  plt.ylabel(u"东坐标")
  
  plt.rcParams['savefig.dpi'] = 300 #图片像素
  plt.rcParams['figure.dpi'] = 300
  #plt.show()
  plt.savefig("C:\\Users\\mushui\\Desktop\\test5\\%s.png"%filename)
  plt.close()
 
print('over!')

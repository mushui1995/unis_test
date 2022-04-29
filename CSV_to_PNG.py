#coding=GBK
import matplotlib.pyplot as plt
import csv
from pylab import *
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker
plt.rcParams['font.sans-serif']=['simhei'] #���������ʾ
plt.rcParams['axes.unicode_minus'] = False
path1="C:\\Users\\mushui\\Desktop\\test2"
#path2="C:\\Users\\mushui\\Desktop\\newpng\\ǧѰ\\5KM\\�����ڵ�"
filelist = os.listdir(path1)
for files in filelist:
 #Olddir = os.path.join(path1,files)
  filename = os.path.splitext(files)[0]#�ļ���
  filetype = os.path.splitext(files)[1]#�ļ���׺
  
  with open(os.path.join(path1,files) ) as f:#������ļ�����������ļ�����洢��f�� 

   reader=csv.reader(f)#����һ���Ķ���reader  
   #header_row=next(reader)
   x_datas=[]
   y_datas=[]
   for row in reader:
	   x_data=float(row[2])
	   x_datas.append(x_data)
	   y_data=float(row[3])
	   y_datas.append(y_data)
	
   #print(x_datas)
    
    #��ƽ��ֵ
  def pingjunzhi(list1):
   sum1 = 0.0
   for item in list1:     
      sum1 += item  
   return sum1/len(list1)
   #���ά�����
  def EWZWC(list1,list2):
   sum1=0.0
   for i in range(0,(len(list1)-1)):
	   sum1=sum1+(list1[i]-pingjunzhi(list1))**2+(list2[i]-pingjunzhi(list2))**2
   ave=np.sqrt(float(sum1/len(list1)))
   return ave
    #Ȧ����ΧԲ
  #def circle(x,y,r,count=2000):
  x=pingjunzhi(x_datas)
  y=pingjunzhi(y_datas)
  #1��
  xarr=[]
  yarr=[]
  rarr=EWZWC(x_datas,y_datas)
  for i1 in range(1,2000):
	  j = float(i1)/2000 * 2 * np.pi
	  xarr.append(x+rarr*np.cos(j))
	  yarr.append(y+rarr*np.sin(j))
  l1,=plt.plot(xarr,yarr,'g.',linewidth=0.1,alpha=0.3)
  #l1=plt.scatter(xarr,yarr,marker = '.', color = 'blue', s = 1,alpha=0.8)
  
  #2��
  xbrr=[]
  ybrr=[]
  rbrr=2*EWZWC(x_datas,y_datas)
  for i2 in range(1,2000):
	  j2 = float(i2)/2000 * 2 * np.pi
	  xbrr.append(x+rbrr*np.cos(j2))
	  ybrr.append(y+rbrr*np.sin(j2))
  l2,=plt.plot(xbrr,ybrr,'b.',linewidth=0.1,alpha=0.2)
  #l2=plt.scatter(xbrr,ybrr,marker = '.', color = 'blue', s = 1,alpha=0.5)
  #3��
  xcrr=[]
  ycrr=[]
  rcrr=3*EWZWC(x_datas,y_datas)
  for i3 in range(1,2000):
	  j3 = float(i3)/2000 * 2 * np.pi
	  xcrr.append(x+rcrr*np.cos(j3))
	  ycrr.append(y+rcrr*np.sin(j3))
  l3,=plt.plot(xcrr,ycrr,'y.',linewidth=0.1,alpha=0.1)
  #l3=plt.scatter(xcrr,ycrr,marker = '.', color = 'blue', s = 1,alpha=0.3)
 
  l1.set_label("��=%r��"%round(rarr,3)) 
  l2.set_label("2��=%r��"%round(rbrr,3)) 
  l3.set_label("3��=%r��"%round(rcrr,3)) 
 
  plt.plot(x_datas, y_datas, 'r.',linewidth=1,alpha=0.5)
  plt.title(u"%s"%filename)
  plt.legend(["��=%r��"%round(rarr,3),"2��=%r��"%round(rbrr,3),"3��=%r��"%round(rcrr,3)],loc=1) 
  plt.xlabel(u"������")
  plt.ylabel(u"������")
  
  plt.rcParams['savefig.dpi'] = 300 #ͼƬ����
  plt.rcParams['figure.dpi'] = 300
  #plt.show()
  plt.savefig("C:\\Users\\mushui\\Desktop\\test5\\%s.png"%filename)
  plt.close()
 
print('over!')

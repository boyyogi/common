# -*- coding: utf-8 -*-

import os
import sys
import  datetime



class Get_data(object):
    def __init__(self,path=os.getcwd()):
        self.path = path
        self.server_list_info = self.server_list()
        self.default_info  = self.default()

    def server_list(self):
        server_list_info = [
            "ac72","ue1","h106"
        ]
        return server_list_info

    def default(self):
        default = {
            "ac72" : 257 ,
            "ue1" : 41 ,
        }
        return default

    def search_file(self):
        dir_list = [ item for item in self.server_list_info if os.path.exists(self.path+"\\hk_speed_"+item)]
        file_list = {}
        for line in dir_list:
            os.chdir(self.path + "\\hk_speed_" + line)
            date_list = os.listdir(".")
            file_list[line] = date_list
        return file_list

    def dispose_file(self,file_list):
        last_data = {}
        for x,y in file_list.items():
            server_data = {}
            for line in y:
                with open(self.path + "\\hk_speed_" + x + "\\" + line +"\\record.txt") as file:
                    for item in file:
                        self.exchange_data(item,x,server_data)
            last_data[x] = server_data.copy()
        return last_data

    def exchange_data(self,data,server,server_data):
        date = datetime.datetime(int(data.split("\t")[0][:4]),int(data.split("\t")[0][4:6]),int(data.split("\t")[0][6:]),\
                                int(data.split("\t")[1].split("-")[0]),int(data.split("\t")[1].split("-")[1]))
        try:
            bandwidth = float(data.split("\t")[2])
        except Exception,err:
            bandwidth = float(0)
        try:
            delay = float(data.split("\t")[-1][:-1])
        except Exception,err:
            delay = self.default_info[server]
        server_data[date] = {
            "bandwidth" : bandwidth ,
            "delay" : delay
                }

    def start(self):
        return self.dispose_file(self.search_file())

from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import datestr2num,DateFormatter
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
import numpy as np
import os

class Draw_hk_speed(Get_data):
    def __init__(self):
        self.data = self.adjust_time()
        super(Draw_hk_speed,self).__init__()
        self.figure_num = 0


    def adjust_time(self):
        new_data = {}
        for x,y in Get_data().start().items():
            date_list = []
            data_tmp = {}
            for i,j in OrderedDict(sorted(y.iteritems(),key=lambda d:d[0])).items():
                if i.date() not in date_list:
                    data_tmp[i.date()] = {i:j}
                    date_list.append(i.date())
                else:
                    data_tmp[i.date()][i] = j
            time_sort = {}
            for key,value in data_tmp.items():
                time_sort[key] = OrderedDict(sorted(value.iteritems(),key=lambda d:d[0]))
            new_data[x] = OrderedDict(sorted(time_sort.iteritems(),key=lambda  d:d[0]))
        return new_data

    def start(self):
        if os.path.exists(self.path + "\\result") == False: os.mkdir(self.path + "\\result")
        for x,y in self.data.items():
            if os.path.exists(self.path+ "\\result\\" + x) == False: os.mkdir(self.path+ "\\result\\" + x)
            for i,j in y.items():
                path_file = self.path+ "\\result\\" + x + "\\" + str(i) +".png"
                self.draw(j,x,path_file)

    def draw(self,data,arg,path_file):
        x = data.keys()
        y = [ data[i]["bandwidth"] for i in x ]
        z = [ data[i]["delay"] for i in x ]
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        mpl.rc('xtick', labelsize=9)  # 设置坐标轴刻度显示大小
        mpl.rc('ytick', labelsize=9)
        font_size = 30
        plt.style.use('ggplot')
        autodates = mdate.AutoDateLocator()
        yearsFmt = mdate.DateFormatter('%H')
        plt.figure(self.figure_num,figsize=(10,10),dpi=400)
        ax1 = plt.subplot(211)
        plt.xlabel(u"时间",size=9)
        plt.ylabel(u"带宽",size=9)
        plt.title(str(arg) + " " + str(x[0].date()))
        # ax1.xaxis.set_major_locator(mdate.HourLocator(byhour=range(24),interval=1))
        # ax1.xaxis.set_major_formatter(yearsFmt)
        # for label in ax1.xaxis.get_ticklabels():
        #     label.set_rotation(45)
        tm_time_list = []
        timedelta = datetime.timedelta(hours=1)
        tm_time = datetime.datetime(x[0].year,x[0].month,x[0].day)
        tm_time_list.append(tm_time)
        for tm in range(24):
            tm_time = tm_time + timedelta
            tm_time_list.append(tm_time)
        plt.xticks(tm_time_list,range(25))
        ax1.plot_date(mdate.date2num(x),y,"r-")
        ax2 = plt.subplot(212)
        plt.xlabel(u"时间",size=9)
        plt.ylabel(u"延迟",size=9)
        # ax2.xaxis.set_major_locator(mdate.HourLocator(byhour=range(24),interval=1))
        # ax2.xaxis.set_major_formatter(yearsFmt)
        plt.xticks(tm_time_list,range(25))
        ax2.plot_date(mdate.date2num(x),z,"b-")
        plt.savefig(path_file)
        self.figure_num += 1
def draw_test():
    x = [datetime.datetime(2016,11,11,5,10),datetime.datetime(2016,11,11,8,20),datetime.datetime(2016,11,11,23,28)]
    y = [10,20,100]
    plt.figure()
    ax1 = plt.subplot(111)
    plt.xticks([datetime.datetime(2016,11,11,0,0,0),datetime.datetime(2016,11,11,8,0,0),datetime.datetime(2016,11,11,16,0,0)],[0,8,16])
    ax1.plot_date(mdate.date2num(x),y,"r-")
    plt.show()
def test():
    aa = Draw_hk_speed()
    aa.start()

if __name__ == "__main__":
    test()
    # draw_test()
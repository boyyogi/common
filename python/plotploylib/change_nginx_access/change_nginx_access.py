#coding=utf-8
import datetime
import  re

class Exchange(object):
    def __init__(self,start_time="",end_time=datetime.datetime.today()):
        self.end_time = self.get_date(end_time)
        if start_time == "":
            add_time = datetime.timedelta(days=60)
            self.start_time = self.end_time - add_time
        else:
            self.start_time = self.get_date(start_time)
    def get_date(self,time):
        return datetime.datetime(int(time.split("-")[0]),int(time.split("-")[1]),int(time.split("-")[2]))

    def change_date_type(self,line):
        nginx_time = line.split(" ")[4]
        nginx_time_type = nginx_time[2:]
        real_time = datetime.datetime.strptime(nginx_time_type, '%d/%b/%Y:%H:%M:%S')
        return real_time
    def get_last_date(self,date_tmp,num):
        keys = date_tmp.keys()
        keys.sort()
        return keys[-num]

    def return_data(self):
        with open("test") as file:
            date_tmp = {}
            detail = {}
            home_num = {}
            [ self.data_exec(line,date_tmp,detail,home_num) for line in file if "Baiduspider" in line ]
            date_tmp[self.get_last_date(date_tmp,1)]["detail"] = detail
            date_tmp[self.get_last_date(date_tmp,1)]["home_num"] = home_num
            return date_tmp


    def data_exec(self,line,date_tmp,detail,home_num):
        real_time = self.change_date_type(line)
        if real_time > self.start_time and real_time < self.end_time:
            if real_time.date() not in date_tmp.keys():
                date_tmp[real_time.date()] = {"sum" : 1}
                if len(date_tmp) == 1:
                    pass
                else:
                    [ detail.setdefault(items,0) for items in range(0,24) if items not in detail.keys() ]
                    [ home_num.setdefault(items,0) for items in range(0,24) if items not in home_num.keys() ]
                    detail_tmp = detail.copy()
                    home_num_tmp = home_num.copy()
                    date_tmp[self.get_last_date(date_tmp,2)]["detail"] = detail_tmp
                    date_tmp[self.get_last_date(date_tmp,2)]["home_num"] = home_num_tmp
                    detail = {}
                    home_num = {}
            else:
                date_tmp[real_time.date()]["sum"] += 1

            if real_time.hour not in home_num.keys():
                if len(re.findall("^/$",line.split(" ")[8])) or  len(re.findall("^/\?",line.split(" ")[8])):
                # if len(re.findall("^/$",line.split(" ")[8])):
                    home_num[real_time.hour] = 1
            else:
                if len(re.findall("^/$",line.split(" ")[8])) or  len(re.findall("^/\?",line.split(" ")[8])):
                # if len(re.findall("^/$",line.split(" ")[8])):
                    home_num[real_time.hour] += 1


            if real_time.hour not in detail.keys():
                detail[real_time.hour] = 1
            else:
                detail[real_time.hour] += 1

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
import numpy as np
import os

class Draw(object):
    def __init__(self,info):
        self.info = info
        print  self.info

    def draw_pic(self):
        num = 1
        for i,j in self.info.items():
            mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            mpl.rc('xtick', labelsize=9)  # 设置坐标轴刻度显示大小
            mpl.rc('ytick', labelsize=9)
            font_size = 30
            plt.style.use('ggplot')
            x = range(0,24)
            y = [ j["detail"][item] for item in x ]
            z = [ j["home_num"][item] for item in x ]
            plt.figure(num)
            plt.subplot(111)
            plt.ylabel(u"数量")
            plt.xlabel(u"小时")
            plt.title(str(i))
            plt.xticks(x)
            plt.plot(x,y,color="red",linewidth=2,linestyle="-",label=u"百度爬虫网站访问量")
            plt.plot(x,z,color="blue",linewidth=1,linestyle="-",label=u"百度爬虫网站首页访问量")
            plt.legend(loc='upper left')
            plt.axis([0,23,0,self.get_max(y)])
            # plt.setp(line,lw=2,mec="g",marker=".")
            # plt.subplt(122)
            # max_num = self.get_max(y)
            # num_tmp = 0
            # explode = []
            # y_tmp = j["detail"].copy()
            # for a,b in y_tmp.items():
            #     if b <= max_num/10:
            #         del y_tmp[a]
            #     num_tmp += 1
            # labels = y_tmp.keys()
            # sizes = y_tmp.values()
            # for item1 in sizes:
            #     if item1 == max_num:
            #         explode.append(0.1)
            #     else:
            #         explode.append(0)
            # plt.pie(sizes,explode=explode, labels=labels,  shadow=True, startangle=90)
            # plt.axis("equal")
            num += 1
            if os.path.exists("e://pic/%s" %i.month) == False:
                os.mkdir("e://pic/%s" %i.month)
            plt.savefig("e://pic/%s/%s" %(i.month,str(i)))


    def get_max(self,list):
        list_tmp = list[:]
        list_tmp.sort()
        return list_tmp[-1]

def test():
    test = Exchange("2016-10-01","2016-12-08")
    info = test.return_data()
    draw = Draw(info)
    draw.draw_pic()




if  __name__ == "__main__":
    test()

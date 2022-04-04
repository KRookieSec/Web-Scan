#-*- coding:utf-8 -*-
from concurrent.futures import thread
import sys
import getopt
import math
from unittest import result
import threading
from binwalk import scan
import requests

#Banner信息，介绍工具
def banner():
    print("*"*51)
    print("*"*2+" "*34+"DirBrute v1.0"+" "*34+"*"*2)
    print("*"*51)
    print("*"*2+" "*22+"Please test after authorization!"+" "*21+"*"*2)
    print("*"*2+" "*31+"Author: SecuritySky"+" "*27+"*"*2)
    print("*"*51)

#使用方法
def usage():
    print("DirBrute help:")
    print("DirBrute.py -u url -t threads -d file")
    print("-h  help")
    print("-u  url")
    print("-t  thread")
    print("-d  dictionary")

#参数获取
def start():
    #如果长度大于等于3
    if len(sys.argv) >= 3:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:t:d:")
        #遍历列表，获取参数
        for k, v in opts:
            if k == "-h":
                help = v
            elif k == "-u":
                url = v
            elif k == "-t":
                threads = v
            elif k == "-d":
                dic =v
        banner()
        multi_scan(url, threads, dic)
    else:
        banner()
        usage()
        sys.exit()

def multi_scan(url, threads, dic):
    result_list = []
    threads_list = []
    #读取字典文件
    with open(dic, "r") as f:
        dic_list = f.readlines()
        #根据线程确定读取的行数，创建线程字典
        if len(dic_list)% int(threads) == 0:
            thread_read_line_num = len(dic_list) / int(threads)
        else:
            thread_read_line_num = math.ceil(len(dic_list) / int(threads))
        i = 0
        temp_list = []
        for line in dic_list:
            i = i+1
            if i % thread_read_line_num == 0:
                temp_list.append(line.strip())
                #如果i对thread_read_line_num取余为0,则将列表内容添加到临时列表中
                result_list.append(temp_list)
                temp_list = []
            else:
                temp_list.append(line.strip())
        #如果取余后列表还剩少于线程数的元素，则对列表进行切片，将剩下的元素单独添加到一个列表
        if len(dic_list) -i < int(threads):
            temp_list.append(dic_list[i:])
            #去除末尾的无效元素
            temp_list.remove(temp_list[-1])
            result_list.append(temp_list)
    #按线程访问字典
    for i in result_list:
        threads_list.append(threading.Thread(target=scan, args=(url,i)))
    for j  in threads_list:
        j.start()

def scan(url, dic):
    #实现扫描功能
    for line in dic:
        r = requests.get(url + '/' + line)
        if r.status_code != 404:
            print(r.url + " ; " + str(r.status_code))

start()
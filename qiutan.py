import importlib
import re
from lxml import etree
import bs4
import urllib3
import requests
from bs4 import BeautifulSoup
import csv
import sys
from lxml import etree
from selenium import webdriver
import time

import pymysql

address = "http://live.win007.com/"


def GetODDS(url):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    browser.get(url)  # 写上自己的链接
    time.sleep(3)  # 缓冲时间，可调
    content = browser.page_source.encode('utf-8')
    #             left_click = browser.find_element_by_css_selector(".ranker.poptip.sort_default_asc.center")#按钮处理
    #             ActionChains(browser).double_click(left_click).perform()

    # soup=BeautifulSoup(content,'html.parser')
    tree = etree.HTML(browser.page_source)
    peilv = []
    captainname = []
    captainname2 = []
    currentMatchTime = []
    socre = []

    oddDic = {}
    trTags = tree.xpath("//*[@id='table_live']")
    for tag in trTags:
        childTree = tag.xpath("./tbody[1]")
        for tag_2 in childTree:
            # childTree_2 = tag_2.xpath("./*[@align='center']")
            childTree_2 = tag_2.xpath("./*[@odds]")
            for tag3 in childTree_2:
                peilv11 = tag3.get("odds")
                peilv.append(peilv11)
            for tag4 in childTree_2:
                captainname.append(tag4.xpath("./td[7]/a[1]/text()")[0])
            for tag_Captain2 in childTree_2:
                captainname2.append(tag_Captain2.xpath("./td[5]/a[3]/text()")[0])
            # for tag_Socre in childTree_2:
            #     if bool(tag_Socre.xpath("./td[6]/text()")[0]):
            #         print(len(socre))
            #         socre.append(tag_Socre.xpath("./td[6]/text()")[0])
            for tag_currentTIme in childTree_2:
                if bool(tag_currentTIme.xpath("./td[4]/text()")[0]):
                    print(len(socre)*10000)
                    currentMatchTime.append(tag_currentTIme.xpath("./td[4]/text()")[0])
                else:
                    print("shibai")
    return peilv, captainname, captainname2, socre, currentMatchTime


def ManageODD():
    oddDic = {}
    odd, cap, cap2, score, Currtime = GetODDS(address)
    for i in range(0, len(cap)):
        oddDic[cap[i]] = odd[i]
        cap2 = score
        Currtime = score
    return oddDic


def DatabaseProcess():
    dataDic = {}
    dataDic = ManageODD()
    # # 打开数据库连接
    db = pymysql.connect("localhost", "root", "szzhqd", "odds", charset='utf8')

    # 使用 cursor() 方法创建一个游标对象 cursor

    for i in dataDic:
        cursor = db.cursor()
        oddInfo = dataDic[i]
        oddArg = oddInfo.split(",")
        Sqlstr = ''
        lens = len(oddArg)
        if lens > 2:
            Sqlstr = 'INSERT INTO ODDSData VALUES (' + ' ' + '"' + str(i) + ' " ' + ',' + oddArg[0] + ',' + oddArg[
                11] + ',' + oddArg[10] + ',' + oddArg[12] + ',' + oddArg[7] + ')'

        else:
            Sqlstr = 'INSERT INTO ODDSData VALUES (' + ' ' + '"' + str(i) + ' " ' + ',' + str(0) + ',' + str(
                0) + ',' + str(
                0) + ',' + str(0) + ',' + str(0) + ')'
        print(Sqlstr)
        cursor.execute(Sqlstr)
        db.commit()
        cursor.close()
    # 关闭数据库连接
    db.commit()
    db.close()


#DatabaseProcess()
GetODDS(address)
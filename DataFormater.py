# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 16:39
# @Author  : HoPGoldy

import win32clipboard as w
import win32con
import re
import random
from ChinassppControl import Chinasspp
from setting import MIN_ADDITION_NUM, MAX_ADDITION_NUM

dataSplitReg = r'━━━━第[0-9]+个条目━━━━[\s]+'
urlReg = '[\S]+(?=\r\n)'
brandReg = r'(?<=宝贝名：\r\n)[\S]+'
titleReg = r'(?<=[\s])[\S]+(?=\r\n长亮点)'
longHighLightsReg = r'(?<=长亮点：\r\n)[\S]+\r\n[\S]+\r\n[\S]+'
shortHighLightReg = r'(?<=短亮点：\r\n)[\S]+\r\n[\S]+\r\n[\S]+'
designHighlightReg = r'(?<=设计亮点\r\n)[\S]+(?=\r\n)'
otherAdditionTitleReg = r'(搭配指南|材质解析)'
otherAdditionContentReg = r'(?<=(搭配指南|材质解析)\r\n)[\S]+'


def getClipBoardData():
    w.OpenClipboard()
    text = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()

    return text


def formatDataByCode(text):
    temps = text.split('^^^')
    datas = []
    for data in temps:
        dataTemps = data.split('|||')
        data = {
            'category': 9,
            'targetPeople': (10, random.randint(1, 5)),
            'url': dataTemps[0],
            'title': dataTemps[1],
            'longHighLight': ('长亮点1长亮点1，长亮点1。', '长亮点2长亮点2，长亮点2。', '长亮点3长亮点3，长亮点3。'),
            'shortHighLight': ('短亮点1短亮点1', '短亮点2短亮点2', '短亮点3短亮点3'),
            'addition': ({
                'title': '设计亮点',
                'content': '设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点设计亮点。'},
                         {
                'title': '品牌介绍',
                'content': '品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍品牌介绍。',
                'brand': 'brand'})
            }
        for i in range(0, len(dataTemps)):
            print(dataTemps[i])


def formatDataByReg(text):
    dataTemps = re.split(dataSplitReg, text)
    datas = []
    for i in range(1, len(dataTemps)):
        dataTemp = dataTemps[i]
        brand = getBrand(dataTemp)
        brandIntroduce = getBrandIntroduce(brand)

        data = {
            'category': 9,
            'targetPeople': (10, random.randint(1, 5)),
            'url': getUrl(dataTemp),
            'title': f'{brand} {getTitle(dataTemp)}',
            'longHighLight': getLongHighLights(dataTemp),
            'shortHighLight': getShortHighLights(dataTemp),
            'addition': ({
                             'title': '设计亮点',
                             'content': getDesignHighlight(dataTemp)},
                         {
                             'title': getOtherAdditionTitle(dataTemp),
                             'content': getOtherAdditionContent(dataTemp)},
                         {
                             'title': '品牌介绍',
                             'content': brandIntroduce,
                             'brand': brand})
            }
        datas.append(data)
    return datas


def show(datas):
    for i in range(0, len(datas)):
        print(f'[检查] ————————————————条目{i + 1}————————————————')
        print(f'[检查] 分类索引 > {datas[i]["category"]}')
        print(f'[检查] 目标人群索引 > {datas[i]["targetPeople"][0]}, {datas[i]["targetPeople"][1]}')
        print(f'[检查] 商品链接 > {datas[i]["url"]}')
        print(f'[检查] 标题 > {datas[i]["title"]}')
        for longHighLight in datas[i]['longHighLight']:
            print(f'[检查] 长亮点 > {longHighLight}')
        for shortHighLight in datas[i]['shortHighLight']:
            print(f'[检查] 短亮点 > {shortHighLight}')
        for addition in datas[i]['addition']:
            if 'brand' in addition:
                print(f'[检查] {addition["title"]}: {addition["brand"]} > {addition["content"]}')
            else:
                print(f'[检查] {addition["title"]} > {addition["content"]}')
        print()


def getUrl(data):
    return re.search(urlReg, data).group(0)


def getBrand(data):
    return re.search(brandReg, data).group(0)


def getTitle(data):
    return re.search(titleReg, data).group(0)


def getLongHighLights(data):
    longHighLightsText = re.search(longHighLightsReg, data).group(0)
    return re.split(r'\r\n', longHighLightsText)


def getShortHighLights(data):
    shortHighLightsText = re.search(shortHighLightReg, data).group(0)
    return re.split(r'\r\n', shortHighLightsText)


def getDesignHighlight(data):
    return re.search(designHighlightReg, data).group(0)


def getOtherAdditionTitle(data):
    return re.search(otherAdditionTitleReg, data).group(0)


def getOtherAdditionContent(data):
    return re.search(otherAdditionContentReg, data).group(0)

def getBrandIntroduce(brandName, min=MIN_ADDITION_NUM, max=MAX_ADDITION_NUM):
    chinasspp = Chinasspp()
    returnBrands = chinasspp.searchBrand(brandName)

    if returnBrands is not None or len(returnBrands) != 0:
        for item in returnBrands:
            introduce = item['introduce']
            if len(introduce) > min and len(introduce) < MAX_ADDITION_NUM:
                return introduce
            elif len(introduce) >= MAX_ADDITION_NUM:
                return cutBrandIntroduce(introduce, min, max)

        return ' ' * MIN_ADDITION_NUM

def cutBrandIntroduce(str, min, max):
    segs = str.split('。')
    goodIntrodue = ''

    for seg in segs:
        goodIntrodue += seg
        if len(goodIntrodue) > min and len(goodIntrodue) < max:
            return goodIntrodue

    return ' ' * MIN_ADDITION_NUM
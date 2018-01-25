import requests
from pymongo import MongoClient
import time
from pyquery import PyQuery as pq
import re

#mongodb服务器的创建
client = MongoClient()
db = client.steam1
ss = db.steam1


def get_discounted_game_info(page):
    url = 'http://store.steampowered.com/search/?specials=1&page='
    for i in range(page):
        newurl = url+str(i)
        print(newurl)
        html = requests.get(newurl).content.decode('utf-8')
        doc = pq(html)
        items = doc('#search_result_container a').items()
        for item in items:
            if item.find('.search_discount.responsive_secondrow').text():
                product = {
                    'title':item.find('.title').text(),
                    'homepage':item.attr('href'),
                    'discount':item.find('.search_discount.responsive_secondrow').text(),
                    'original_price':item.find('.search_price.discounted.responsive_secondrow span').text(),
                    'publish_date':item.find('.search_released.responsive_secondrow').text(),
                    'image':item.find('img').attr('src'),
                }
                ss.insert(product) #将结果存入数据库
                print(product)     #将结果打印

if __name__=='__main__':
    get_discounted_game_info(55)#页数可以自定义

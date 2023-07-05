#coding:utf8
from bs4 import BeautifulSoup

from bs4 import BeautifulSoup, NavigableString

from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
import re
import json

from bs4 import BeautifulSoup
import requests
import json


def get_soup_from_url(url):
    # 发送GET请求
    response = requests.get(url,verify=False)

    # 创建一个BeautifulSoup对象，获取页面正文
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def extract_by_keyword(soup, keyword):
    # 创建一个空的字典
    result = {}

    # 在soup对象中查找关键词
    tags = soup.find_all(string=lambda text: keyword in text.lower())

    # 根据关键词类型处理
    if keyword == 'email':
        result[keyword] = [tag.find_parent('a')['href'] for tag in tags]
    elif keyword == 'positions':
        result[keyword] = [tag.text.strip() for tag in tags[0].find_next('dl').find_all('dd')]
    elif keyword == 'publications':
        result[keyword] = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
    elif keyword == 'достижения':
        result[keyword] = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
    elif keyword == 'clinical trials':
        result[keyword] = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
    else:
        print(f"No handler for keyword '{keyword}'")

    return result

def extract_by_keyword_tag(soup, keyword,tag_type):
    # 创建一个空的字典
    result = {}

    # 在soup对象中查找关键词
    tags = soup.find_all(string=lambda text: keyword in text.lower())

    def get_li_data(keyword):
        res = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
        return res
    def get_dd_data(keyword):
        res = result[keyword] = [tag.text.strip() for tag in tags[0].find_next('dl').find_all('dd')]
        return res

    def get_ap_data(keyword):
        res = [tag.find_parent('a')['href'] for tag in tags]
        return res

    def handler(keyword,tag_type):
        res=None
        if tag_type == 'ap':
            res = get_ap_data(keyword)
        if tag_type == 'dd':
            res = get_dd_data(keyword)
        if tag_type == 'li':
            res = get_li_data(keyword)
        return res

    # 根据关键词类型处理
    if keyword in ['ap','dd','li']:
        result[keyword] = handler(keyword,tag_type)
    else:
        print(f"No handler for keyword '{keyword}'")

    return result

# 用URL获取soup对象
# soup = get_soup_from_url('https://www.bcm.edu/people-search/thomas-kosten-24837')  # ok，隐藏的不行
# soup = get_soup_from_url('https://profiles.stanford.edu/john-ioannidis')  # ok，隐藏的不行
soup = get_soup_from_url('http://www.mc.msu.ru/about/doctors/doctor/?ID=404')  # ok，隐藏的不行
# soup = get_soup_from_url('https://profiles.uchicago.edu/profiles/display/37485') # bad
# soup = get_soup_from_url('https://support.psyc.vt.edu/users/wkbickel')  # ok

# 提取关键词信息
# result = extract_by_keyword(soup, 'publications')
result = extract_by_keyword(soup, 'достижения')
# result = extract_by_keyword(soup, 'clinical trials')
print(result)

# # 示例的HTML
# with open("data/clean.txt", "r", encoding='utf8') as f:
#     html = f.read()


# # 输出结果
# print(json.dumps(result, indent=4))
#
# # with open("ss_0.txt","r",encoding='utf8') as f:
# #     html = f.read()
#
# # print(html.encode())
#
# res = extract_info_from_html(html,'publications')
# print(res)
# res = extract_info_from_html(html,'email')
# print(res)
# res = extract_info_from_html(html,'positions')
# print(res)
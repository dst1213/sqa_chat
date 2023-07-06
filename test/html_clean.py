#coding:utf8
"""
抓取的html数据清洗和压缩 - 简书
https://www.jianshu.com/p/6c6fe17073d7


"""
import requests
from lxml.html import clean
# 除了保留的attribute其他的删除
safe_attrs = frozenset(['controls', 'poster', 'src', 'href', 'alt'])
# 默认删除script之类的无用标签，若需保留则添加scripts=False
# 默认删除的有<script>, javascript, comments, style, <link>, <meta>等
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs)

# url = "https://support.psyc.vt.edu/users/wkbickel"
# url = "https://www.tristarhealth.com/physicians/profile/Dr-David-R-Spigel-MD"
# url = "https://icahn.mssm.edu/profiles/aneel-k-aggarwal"
# url = "https://www.pennmedicine.org/providers/profile/corey-langer" # 基本空
# url = "https://profiles.stanford.edu/john-ioannidis"
# url = "https://www.hopkinsmedicine.org/profiles/details/lisa-cooper"
# url = "http://www.mc.msu.ru/about/doctors/doctor/?ID=404"
url = "https://scholars.lib.ntu.edu.tw/cris/rp/rp06754"
# url = "https://www.uchicagomedicine.org/find-a-physician/physician/marina-chiara-garassino#"
# url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
# url = "https://profiles.uchicago.edu/profiles/display/37485"


# response = requests.get(url,verify=False)

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def get_html_by_sn(url):
    # 获取所有展示的文本内容和原始结构
    # 引入浏览器配置
    options = webdriver.ChromeOptions()
    # 设置无头模式
    options.add_argument('--headless')  # 不打开浏览器
    # 启动浏览器实例，添加配置信息
    browser = webdriver.Chrome(options=options)
    # browser = webdriver.Chrome()
    browser.get(url)
    html_text = browser.page_source
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    output = ""
    for t in text.split("\n"):
        if t.replace(" ", "").replace("\t", "") == "":
            continue
        output += t
        output += "\n"
    browser.quit()
    return soup, output, html_text

_,_,html_text = get_html_by_sn(url)

# content = cleaner.clean_html(response.text)
content = cleaner.clean_html(html_text)

import htmlmin
content = htmlmin.minify(content, remove_comments=True, remove_all_empty_space=True)

with open("data/SHIH-JUNG-CHENG_html.txt", "w", encoding="utf8") as f:
    f.write(content)

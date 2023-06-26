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
# url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
url = "https://profiles.uchicago.edu/profiles/display/37485"
response = requests.get(url,verify=False)
content = cleaner.clean_html(response.text)

import htmlmin
content = htmlmin.minify(content, remove_comments=True, remove_all_empty_space=True)

with open("data/Zacny.txt", "w", encoding="utf8") as f:
    f.write(content)

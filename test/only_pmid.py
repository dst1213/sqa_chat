import re

import requests

from lxml.html import clean
# 除了保留的attribute其他的删除
safe_attrs = frozenset(['controls', 'poster', 'src', 'href', 'alt'])
# 默认删除script之类的无用标签，若需保留则添加scripts=False
# 默认删除的有<script>, javascript, comments, style, <link>, <meta>等
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs)

html_string = """ ... """  # 这里应该是HTML文本
# with open("data/Zacny.txt", "r", encoding="utf8") as f:
#     text = f.read()

# url = "https://profiles.uchicago.edu/profiles/display/37485"
url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
response = requests.get(url,verify=False)
html = response.text
content = cleaner.clean_html(response.text)
pattern = r'<a href=(")?(https?:)?//(www\.)?ncbi.nlm.nih.gov/pubmed/(\?term=)?(\d+)'
matches = re.findall(pattern, content)

for match in matches:
    pmid = match[-1]  # PMID是最后一个捕获组
    full_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"  # 生成完整链接
    print(f'PMID: {pmid}, Link: {full_link}')

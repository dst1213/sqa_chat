import requests
from bs4 import BeautifulSoup

from log_tools import slogger


def get_html(url):
    response = requests.get(url, verify=False)  # 解决中肿网页Https无法爬取
    soup = BeautifulSoup(response.content, 'html.parser')
    # 从HTML中提取出文本内容并去除换行、空格等字符
    # text = soup.get_text().replace('\n', '').replace('\r', '').replace('\t', '').strip()
    text = soup.get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    # text = soup.get_text().replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t').strip()
    # with open("test/data/Zacny.html.txt",'r',encoding='utf8') as f:
    #     text = f.read()
    slogger.info(f"type:{type(text)},text:{text}")
    return soup, text, response.text

url = "https://locations.ecuhealth.org/Providers/details/16"
_,text,_ = get_html(url)
with open("data/test.txt","w",encoding="utf8") as f:
    f.write(text)
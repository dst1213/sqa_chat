#coding:utf8
import requests
from bs4 import BeautifulSoup
import json

from test.html_clean import cleaner


def fuzzy_search_extract(soup, keyword):
    result_dict = {keyword: []}

    # 查找包含关键词的节点
    elements = soup.body(text=lambda text: keyword in text)

    # 对于找到的每一个节点
    for elem in elements:
        # 如果它是一个tag
        if keyword.lower() in elem.parent.name.lower():
            # 抽取所有的子节点文本和链接
            sub_elements = elem.parent.find_all()
            for sub_elem in sub_elements:
                if sub_elem.name == 'a':
                    result_dict[keyword].append(sub_elem['href'])
                else:
                    result_dict[keyword].append(sub_elem.text)
        # 如果它是文本
        elif keyword.lower() in elem.lower():
            for n in elem.parent.next_siblings:
                print(n.text.strip())
                print(elem.parent.text.strip())
                result_dict[keyword].append(n.text.strip())
    print(result_dict)
    # return json.dumps(result_dict, ensure_ascii=False)
    return result_dict


# 示例的HTML
# url = "https://profiles.uchicago.edu/profiles/display/37485"
url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
response = requests.get(url,verify=False)
html = response.text
# content = cleaner.clean_html(response.text)
soup = BeautifulSoup(html, 'html.parser')
res = fuzzy_search_extract(soup, 'publications')
# print(res)

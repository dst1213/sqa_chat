# coding:utf-8
import timeout_decorator  # pip install timeout-decorator
from retrying import retry
import warnings
import platform
import re

import requests

from lxml.html import clean
from common import *

BAOSTOCK_TIMEOUT = 3  # baostock超时，秒
BAOSTOCK_RETRY = 3  # baostock重试次数,3
BAOSTOCK_WAIT_INTERVAL = 3000  # ms毫秒，wait_fixed 设置失败重试的间隔时间,2000
class BaostockUtils:

    @staticmethod
    def exception(e):
        return isinstance(e, Exception)

# 最终版，超时后自动重试，支持windows（不做超时和重试）和Linux
def timeout_and_retry(timeout=3, wait_fixed=4000, stop_max_attempt_number=3, retry_on_exception=None,
                      suppress_warn=False):
    def decorator(func):
        def caller(*args, **kwargs):
            _sys = platform.system()
            if _sys != 'Windows':
                td = timeout_decorator.timeout(timeout)(func)
                rt = retry(wait_fixed=wait_fixed, stop_max_attempt_number=stop_max_attempt_number,
                           retry_on_exception=retry_on_exception)(td)
                res = rt(*args, **kwargs)
            else:
                if suppress_warn:
                    warnings.warn(f"timeout_and_retry don't support {_sys}!")
                res = func(*args, **kwargs)
            return res

        return caller

    return decorator

def split_text(text, limit):
    parts = []
    while len(text) > limit:
        part = text[:limit]
        last_newline_pos = part.rfind('\n')
        if last_newline_pos >= 0:
            part = part[:last_newline_pos]
        parts.append(part)
        text = text[len(part) + 1:]  # +1 to skip the newline
    parts.append(text)
    return parts


def handle(text,model_type='gpt-3.5-turbo',out_type='json'):
    # 你的handle函数，这里只是一个示例
    result = {}
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L1
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L2
    prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L3
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L4
    try:
        if model_type != 'text-davinci-003':
            result = get_data(text, prompt, model=model_type)  # gpt-3.5-turbo-16k
        else:
            result = get_data_davinci(text, prompt, model='text-davinci-003')  # gpt-3.5-turbo-16k
        slogger.info(f"result:{result}")
        if out_type == 'json':
            result = json.loads(result)
    except Exception as e:
        slogger.error(f"handle error:{e}")  # chatgpt返回的json可能格式是错的，要重试
        try:
            slogger.error(f"try again......")
            if model_type != 'text-davinci-003':
                result = get_data(text, prompt, model=model_type)  # gpt-3.5-turbo-16k
            else:
                result = get_data_davinci(text, prompt, model='text-davinci-003')  # gpt-3.5-turbo-16k
            slogger.info(f"result:{result}")
            if out_type == 'json':
                result = json.loads(result)
        except Exception as e:
            slogger.error(f"handle error:{e}")
    return result


def merge_results(results, to_str=True, synonym=True,nodup=True):
    field_synonym = {"name": ["姓名", "name"],
                     "organization": ["医院机构", "诊所", "药厂", "公司", "hospital", "clinic"],
                     "department": ["科室", "部门", "department"],
                     "position": ["职务", "职位", "position"],
                     "title": ["职称", "title"],
                     "phone": ["电话", "contact", "phone", "mobile"],
                     "email": ["邮箱", "email", "电邮"],
                     "location": ["位置", "地址", "城市", "location", "office location"],
                     "introduce": ["个人介绍", "自我介绍", "专家介绍", "简介", "about me", "introduce"],
                     "expertise": ["专长：", "擅长", "specialty", "expertise"],
                     "visit time": ["出诊时间", "出诊信息", "visit time", "visit hours"],
                     "qualification": ["资格证书", "qualification"],
                     "insurance": ["适用医保", "医疗保险", "医保", "insurance"],
                     "academic": ["学术兼职", "part-time", "academic"],
                     "work_experience": ["工作经历", "work experience", "career"],
                     "education": ["学习经历", "学历", "education"],
                     "publications": ["文献著作", "出版", "论文", "publications"],
                     "clinical_trial": ["临床研究", "研究", "clinical_trial", "clinical trial"],
                     "achievement": ["荣誉成就", "honor", "achievement"]}
    merged = {}
    for result in results:
        slogger.info(f"merge_results result:type:{type(result)}, result:{result}")
        if result and isinstance(result,dict):
            for key, value in result.items():
                if value:
                    if key.lower() in merged:
                        if isinstance(value, list):
                            merged[key.lower()].extend(value)
                        else:
                            merged[key.lower()].append(value)
                    else:
                        merged[key.lower()] = []
                        if isinstance(value, list):
                            merged[key.lower()].extend(value)
                        else:
                            merged[key.lower()].append(value)


    if synonym:
        syn_merged = {k: [] for k, v in field_synonym.items()}
        for k, v in merged.items():
            for sk, sv in field_synonym.items():
                if k.lower() in sv:
                    syn_merged[sk].extend(v)
                    break
        merged = syn_merged
        slogger.info(f"synonym merged:{merged}")

    if nodup:
        new_merged={}
        for k,v in merged.items():
            try:
                new_merged[k] = list(set(merged[k])) if isinstance(merged[k],list) else merged[k]
            except Exception as e:
                slogger.error(f"new_merged error:{e}")
                traceback.print_exc()
                new_merged[k] = merged[k]

        merged = new_merged
        slogger.info(f"nodup merged:{merged}")

    if to_str:
        for k, v in merged.items():
            merged[k] = ','.join([str(x) for x in v]) if isinstance(v, list) else str(v)
    return merged


def long_text_extractor(text, limit=4000, repeat=0, out_type='json',to_str=True, model_type='gpt-3.5-turbo',url=None):
    results = []
    split_parts = split_text(text, limit)
    for i in range(repeat + 1):
        for idx,part in enumerate(split_parts,1):
            slogger.info(f"======================第{idx}/{len(split_parts)}个片段===========================")
            try:
                result = handle(part,model_type=model_type,out_type=out_type)
                if result:
                    results.append(result)
                # time.sleep(30)  # cloudflare 504
                time.sleep(3)  # cloudflare 504
            except Exception as e:
                slogger.error(f"long_text_extractor error:{e}")
    if out_type == 'json':
        merged = merge_results(results)
        merged['pmid'] = ','.join(get_pubmed_id_link(url=url))
        slogger.info(f"merged:{merged}")
    else:
        results = list(set(results))
        merged = '\n'.join(results)
        merged += '\npmid:'+ ','.join(get_pubmed_id_link(url=url))
        slogger.info(f"merged:{merged}")
    return merged


def get_pubmed_id_link(html=None,url=None):
    # 除了保留的attribute其他的删除
    safe_attrs = frozenset(['controls', 'poster', 'src', 'href', 'alt'])
    # 默认删除script之类的无用标签，若需保留则添加scripts=False
    # 默认删除的有<script>, javascript, comments, style, <link>, <meta>等
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs)

    html_string = """ ... """  # 这里应该是HTML文本
    # with open("data/Zacny.txt", "r", encoding="utf8") as f:
    #     text = f.read()
    content=None
    pmids = []

    try:
        if url:
            # url = "https://profiles.uchicago.edu/profiles/display/37485"
            # url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
            response = requests.get(url,verify=False)
            # html = response.text
            content = cleaner.clean_html(response.text)
        elif html:
            # 注意html文本必须清洗过，否则可能提取有问题
            content = cleaner.clean_html(html)

        pattern = r'<a href=(")?(https?:)?//(www\.)?ncbi.nlm.nih.gov/pubmed/(\?term=)?(\d+)'
        matches = re.findall(pattern, content)

        for match in matches:
            pmid = match[-1]  # PMID是最后一个捕获组
            full_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"  # 生成完整链接
            print(f'PMID: {pmid}, Link: {full_link}')
            pmids.append(pmid)
        pmids = list(set(pmids)) if pmids else pmids
        slogger.info(f"len pmids:{len(pmids)}")
    except Exception as e:
        slogger.error(f"get_pubmed_id_link error:{e}")
    return pmids

if __name__ == "__main__":
    text = "这里是你的长文本"  # 请将此处替换为你的长文本
    with open("test/data/Zacny.html.txt",'r',encoding='utf8') as f:
        text = f.read()
    # get_pubmed_id_link(url="https://profiles.uchicago.edu/profiles/display/37485")
    # get_pubmed_id_link(url="https://sbmi.uth.edu/faculty-and-staff/dean-sittig.htm")
    get_pubmed_id_link(url="https://www.hopkinsmedicine.org/profiles/details/lisa-cooper") # TUN

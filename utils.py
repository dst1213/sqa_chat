# coding:utf-8
import markdown
import timeout_decorator  # pip install timeout-decorator
from bs4 import BeautifulSoup
from retrying import retry
import warnings
import platform
import re
import htmlmin
import html2text
import requests
from lxml.html import clean
from llm_tools import *
from langchain.text_splitter import MarkdownHeaderTextSplitter

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


def llm_handler(text, model_type='gpt-3.5-turbo', out_type='json', prompt=prompts.FIELD_EXTRACTOR_TEMPLATE_L3):
    # 你的handle函数，这里只是一个示例
    result = {}
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L1
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L2
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L3
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L4
    try:
        if model_type != 'text-davinci-003':
            result = get_openai_data(text, prompt, model=model_type)  # gpt-3.5-turbo-16k
        else:
            result = get_openai_data_davinci(text, prompt, model='text-davinci-003')  # gpt-3.5-turbo-16k
        slogger.info(f"result:{result}")
        if out_type == 'json':
            result = json.loads(result)
    except Exception as e:
        slogger.error(f"llm_handler error:{e}")  # chatgpt返回的json可能格式是错的，要重试
        try:
            slogger.error(f"try again......")
            if model_type != 'text-davinci-003':
                result = get_openai_data(text, prompt, model=model_type)  # gpt-3.5-turbo-16k
            else:
                result = get_openai_data_davinci(text, prompt, model='text-davinci-003')  # gpt-3.5-turbo-16k
            slogger.info(f"result:{result}")
            if out_type == 'json':
                result = json.loads(result)
        except Exception as e:
            slogger.error(f"llm_handler error:{e}")
    return result


def merge_results(results, to_str=True, synonym=True, nodup=True):
    # 映射关系总表：大于ChatGPT的Prompt，大于产品关键词表，多了网页特有的表述
    field_synonym = {"name": ["姓名", "name"],
                     "organization": ["医院机构", "诊所", "药厂", "公司", "hospital", "clinic"],
                     "department": ["科室", "部门", "department"],
                     "position": ["职务", "职位", "position"],
                     "title": ["职称", "title"],
                     "phone": ["电话", "contact", "phone", "mobile"],
                     "email": ["邮箱", "email", "电邮"],
                     "location": ["位置", "地址", "城市", "location", "office location"],
                     "introduce": ["个人介绍", "自我介绍", "专家介绍", "简介", "about me", "introduce","biology"],
                     "expertise": ["专长：", "擅长", "specialty", "expertise", "interests"],
                     "visit_time": ["出诊时间", "出诊信息", "visit time", "visit hours"],
                     "qualification": ["资格证书", "qualification"],
                     "insurance": ["适用医保", "医疗保险", "医保", "insurance"],
                     "academic": ["学术兼职", "part-time", "academic"],
                     "work_experience": ["工作经历", "work experience", "career", "short bio"],
                     "education": ["学习经历", "学历", "education"],
                     "publications": ["文献著作", "出版", "论文", "publications","abstract","all publications","selected publications"],
                     "clinical_trial": ["临床研究", "研究", "clinical_trial", "clinical trials"],
                     "achievement": ["荣誉成就", "honor", "achievement"],
                     "service_language": ["服务语言", "service language", "language"]}
    merged = {}
    for result in results:
        slogger.info(f"merge_results total:{len(results)}, result type:{type(result)}, result:{result}")
        if result and isinstance(result, dict):
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
    slogger.info(f"merged result:{merged}")
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
        new_merged = {}
        for k, v in merged.items():
            try:
                new_merged[k] = list(set(merged[k])) if isinstance(merged[k], list) else merged[k]
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


def llm_text_extractor(text, limit=4000, repeat=0, out_type='json', to_str=True, model_type='gpt-3.5-turbo', url=None,
                       prompt=prompts.FIELD_EXTRACTOR_TEMPLATE_L3):
    results = []
    split_parts = split_text(text, limit)
    for i in range(repeat + 1):
        for idx, part in enumerate(split_parts, 1):
            slogger.info(f"======================第{idx}/{len(split_parts)}个片段===========================")
            try:
                result = llm_handler(part, model_type=model_type, out_type=out_type, prompt=prompt)
                if result:
                    results.append(result)
                # time.sleep(30)  # cloudflare 504
                time.sleep(3)  # cloudflare 504
            except Exception as e:
                slogger.error(f"llm_text_extractor error:{e}")
    return results


def rule_text_extractor(text, tag_text,url=None):
    # PMID
    pmids = []
    _pmids = get_pubmed_id_link(html=tag_text)
    if _pmids:
        pmids.extend(_pmids)

    _pmids2 = extract_pubmed_ids(text)
    if _pmids2:
        pmids.extend(_pmids2)

    # PMCID
    pmcids = []
    _pmcids = extract_pmc_ids(text)
    if _pmcids:
        pmcids.extend(_pmcids)

    # Publications
    publications = []
    # 用URL获取soup对象
    # soup = get_soup_from_url(url)
    soup = get_soup_from_text(tag_text)
    # 提取关键词信息
    _pub_keyword = 'publications'
    _pubs = extract_by_keyword(soup, _pub_keyword)
    if _pubs:
        publications.extend(_pubs[_pub_keyword])

    # Clinical trials
    ct = []
    # 用URL获取soup对象
    # soup = get_soup_from_url(url)
    soup = get_soup_from_text(tag_text)
    # 提取关键词信息
    _ct_keyword = 'clinical trials'
    _ct = extract_by_keyword(soup, _ct_keyword)
    if _ct:
        ct.extend(_ct[_ct_keyword])

    return {"pmids": pmids, "pmcids": pmcids, "publications": publications, "clinical_trials": ct}


def merge_strategy(llm_results, md_results, rule_results, out_type='json', force_json=False):
    if force_json:
        slogger.info(f"before repair_json:{llm_results}")
        llm_results = [repair_json(result) for result in llm_results]
        slogger.info(f"after repair_json:{llm_results}")
        out_type = 'json'
    if out_type == 'json':
        results = llm_results + md_results
        merged = merge_results(results)
        merged['pmid'] = ','.join(rule_results['pmids'])
        merged['pmcid'] = ','.join(rule_results['pmcids'])
        merged['articles'] = ','.join(rule_results['publications'])
        merged['clinical_trials'] = ','.join(rule_results['clinical_trials'])
        slogger.info(f"merged:{merged}")
    else:
        results = list(set(llm_results + md_results))
        merged = '\n'.join(results)
        merged += '\npmid:' + ','.join(rule_results['pmids'])
        merged += '\npmcid:' + ','.join(rule_results['pmcids'])
        merged += '\narticles:' + ','.join(rule_results['publications'])
        merged += '\nclinical_trials:' + ','.join(rule_results['clinical_trials'])
        slogger.info(f"merged:{merged}")
    return merged


def verify_truth():
    """
    校验：信息丢失、信息冗余（多）、信息不对、信息错位【A字段填到B字段，可能是A,B字段相似度较高导致】
    步骤：GPT抽取信息（循环5次）-> Omission缺失查找 -> Evidence证据补全（就是抽取的实体附上原文） -> Prune剪枝去掉错误不准确的信息

    微软的论文和代码
    [2306.00024] Self-Verification Improves Few-Shot Clinical Information Extraction
    https://arxiv.org/abs/2306.00024
    microsoft/clinical-self-verification: Self-verification for LLMs.
    https://github.com/microsoft/clinical-self-verification

    # TODO
    超长文本如何用ChatGPT校验，token限制，抽样？
    Evidence也不好弄

    """
    pass


def web_text_extractor(text, raw_text=None,limit=4000, repeat=0, out_type='json', to_str=True, model_type='gpt-3.5-turbo', url=None):
    # step0: 带格式的网页清理
    tag_text = html_clean(url,raw_text)

    # step1: Rule template规则模板抽取
    rule_results = rule_text_extractor(text, tag_text, url)
    # step2: Markdown模板匹配
    keywords = ["bio", "biology", "publications", "clinical trials", "abstract"]
    md_results = markdown_text_extractor(tag_text,url, keywords=keywords)
    # step3: LLM抽取（兜底），不同的网页可能需要不同的Prompt template模板，甚至需要通用模板+定制模板两轮
    llm_results = llm_text_extractor(text, limit, repeat, out_type, to_str, model_type, url,
                                     prompt=prompts.FIELD_EXTRACTOR_TEMPLATE_L3)
    # _llm_results = llm_text_extractor(text, limit, repeat, out_type, to_str, model_type, url,prompt=prompts.FIELD_EXTRACTOR_TEMPLATE_L3)
    # llm_results.extend(_llm_results)
    # step4: 数据融合策略
    merged = merge_strategy(llm_results, md_results, rule_results, out_type, force_json=True)
    # step5: verify_truth【去重放到merge做，循环ChatGPT要做，校验要做】
    verify_truth()
    return merged


def get_pubmed_id_link(html=None, url=None):
    # 除了保留的attribute其他的删除
    safe_attrs = frozenset(['controls', 'poster', 'src', 'href', 'alt'])
    # 默认删除script之类的无用标签，若需保留则添加scripts=False
    # 默认删除的有<script>, javascript, comments, style, <link>, <meta>等
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs)

    html_string = """ ... """  # 这里应该是HTML文本
    # with open("data/Zacny.txt", "r", encoding="utf8") as f:
    #     text = f.read()
    content = None
    pmids = []

    try:
        if url:
            # url = "https://profiles.uchicago.edu/profiles/display/37485"
            # url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
            response = requests.get(url, verify=False)
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


def extract_pubmed_ids(text):
    pattern = r"(?:PubMed (?:PMID): |PMID: |^|PMID:)(\d+)"

    pmids = re.findall(pattern, text)
    slogger.info(f"extract_pubmed_ids len:{len(pmids)}")
    return pmids


def extract_pmc_ids(text):
    # pattern = r"(?:PubMed (?:PMID|Central PMCID): |PMID: |^)(\d+)"
    pattern = r"(?:PubMed (?:Central PMCID): )(PMC\d+)"

    pmcids = re.findall(pattern, text)
    slogger.info(f"extract_pmc_ids len:{len(pmcids)}")
    return pmcids


def get_soup_from_url(url):
    # 发送GET请求
    response = requests.get(url, verify=False)

    # 创建一个BeautifulSoup对象，获取页面正文
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def get_soup_from_text(text):


    # 创建一个BeautifulSoup对象，获取页面正文
    soup = BeautifulSoup(text, 'html.parser')

    return soup

def extract_by_keyword(soup, keyword):
    # 创建一个空的字典
    result = {}

    # 在soup对象中查找关键词
    tags = soup.find_all(string=lambda text: keyword in text.lower())
    try:
        # 根据关键词类型处理
        if keyword == 'email':
            result[keyword] = [tag.find_parent('a')['href'] for tag in tags]
        elif keyword == 'positions':
            result[keyword] = [tag.text.strip() for tag in tags[0].find_next('dl').find_all('dd')]
        elif keyword == 'publications':
            result[keyword] = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
        elif keyword == 'clinical trials':
            result[keyword] = [tag.text.strip() for tag in tags[0].find_next('ul').find_all('li')]
        else:
            print(f"No handler for keyword '{keyword}'")
    except Exception as e:
        result[keyword] = []
        slogger.error(f"extract_by_keyword error:{e}")

    slogger.info(f"extract_by_keyword result: {result}")
    return result


def repair_json(data):
    n = 0
    max_retries = 10
    while n < max_retries:
        n += 1
        try:
            # Try to load the string as a JSON
            _data = json.loads(data)
            return _data  # return if it is a valid JSON
        except json.JSONDecodeError:
            # If JSON is invalid, find the last valid opening mark and cut the string
            open_position = max(data.rfind("{"), data.rfind("["), data.rfind('"'))
            close_position = max(data.rfind("}"), data.rfind("]"), data.rfind('"'))

            # Check for unbalanced quotes
            quote_count = data.count('"')
            unbalanced_quotes = quote_count % 2 != 0

            left_bracket_count = data.count("[")
            right_bracket_count = data.count("]")
            unbalanced_brackets = left_bracket_count != right_bracket_count

            if open_position > close_position:
                if unbalanced_quotes and data[open_position] == '"':
                    # If last opening mark is a quote and quotes are unbalanced, add closing quote
                    data = data[:open_position + 1] + '"'
                else:
                    # If last opening mark is a bracket, remove it
                    data = data + ']' if data[-1] == '[' else data[:open_position]
            else:
                if unbalanced_quotes and data[close_position] == '"':
                    # If last closing mark is a quote and quotes are unbalanced, remove it
                    data = data[:close_position]
                else:
                    # If last closing mark is a bracket, add corresponding closing bracket
                    # bracket = "}" if data[close_position] == "]" else "]"
                    bracket = ""
                    if (data[close_position] == "]" or data[close_position] == '"') and not unbalanced_brackets:
                        bracket = "}"
                    elif unbalanced_brackets:
                        bracket = "]"

                    data = data[:close_position + 1] + bracket

            # If no valid opening mark found, assume the JSON string is too broken and return an empty dict
            if open_position == -1 and close_position == -1:
                return {}


def md2txt(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.get_text()
    return txt


def doc_obj_to_text(doc_obj):
    txt = ''
    try:
        txt = md2txt(doc_obj["content"]) if isinstance(doc_obj,dict) else md2txt(doc_obj.page_content)
        slogger.info(f"doc_obj_to_text:{txt}")
    except Exception as e:
        slogger.error(f"doc_obj_to_text error:{e}")
    return txt


def md_splitter(txt):
    md_header_splits = None
    # markdown template
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
    ]
    try:
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(txt)
    except Exception as e:
        slogger.error(f"html_clean error:{e}")
    return md_header_splits


def html_clean(url=None,raw_text=None):
    content = None
    try:
        # 除了保留的attribute其他的删除
        safe_attrs = frozenset(['controls', 'poster', 'src', 'href', 'alt'])
        # 默认删除script之类的无用标签，若需保留则添加scripts=False
        # 默认删除的有<script>, javascript, comments, style, <link>, <meta>等
        cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs)

        # url = "https://support.psyc.vt.edu/users/wkbickel"
        if not raw_text:
            response = requests.get(url, verify=False)
            tag_text= response.text
        else:
            tag_text = raw_text
        content = cleaner.clean_html(tag_text)

        content = htmlmin.minify(content, remove_comments=True, remove_all_empty_space=True)
    except Exception as e:
        slogger.error(f"html_clean error:{e}")
    return content


def html2md(html_doc):
    res = None
    try:
        res = html2text.html2text(html_doc)
    except Exception as e:
        slogger.error(f"html2md error:{e}")
    return res


def markdown_text_extractor(html_doc, url, keywords):
    result = []
    try:
        # html_doc = html_clean(url)
        md_txt = html2md(html_doc)
        res = markdown_handler(md_txt, keywords)
        result.append(res)
        slogger.info(f"markdown_text_extractor:{result}")
    except Exception as e:
        slogger.error(f"markdown_text_extractor error:{e}")
    return result


def markdown_handler(md_txt, keywords):
    """
    Document(page_content='Dr. Aggarwal is an internationally recognized structural biologist',
    metadata={'Header 1': 'Business Office', 'Header 2': '__Business Office 1', 'Header 3': 'Biography'})
    :param md_txt:
    :return:
    """
    if not keywords:
        return
    result = {keyword: [] for keyword in keywords}
    try:
        ms_doc_objs = md_splitter(md_txt)
    except Exception as e:
        slogger.error(f"markdown_text_extractor md_splitter error:{e}")
        return
    for doc_obj in ms_doc_objs:
        try:
            content = doc_obj_to_text(doc_obj)
            meta = doc_obj["metadata"] if isinstance(doc_obj,dict) else doc_obj.metadata   # 218版的Langchain是Document对象page_content
            for keyword in keywords:
                try:
                    meta_values = [v.lower() for v in meta.values()]
                    if keyword.lower() in meta_values:
                        result[keyword].append(content)
                except Exception as e:
                    slogger.error(f"markdown_text_extractor keyword error:{e}")
        except Exception as e:
            slogger.error(f"markdown_text_extractor doc_obj error:{e}")
    return result


if __name__ == "__main__":
    text = "这里是你的长文本"  # 请将此处替换为你的长文本
    with open("test/data/Zacny.html.txt", 'r', encoding='utf8') as f:
        text = f.read()
    # get_pubmed_id_link(url="https://profiles.uchicago.edu/profiles/display/37485")
    # get_pubmed_id_link(url="https://sbmi.uth.edu/faculty-and-staff/dean-sittig.htm")
    get_pubmed_id_link(url="https://www.hopkinsmedicine.org/profiles/details/lisa-cooper")  # TUN

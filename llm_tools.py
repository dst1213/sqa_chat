import copy
import json
import os
import time
import traceback
import sqlite3
from functools import reduce
from typing import List

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from llama_index import LangchainEmbedding, OpenAIEmbedding
import requests

import config
import prompts
from log_tools import slogger
from dotenv import load_dotenv

load_dotenv()

# api_key = os.environ.get("OPENAI_API_KEY")
# api_host = os.environ.get("OPENAI_API_BASE")
# api_host_bak = os.environ.get("OPENAI_API_BASE_BACKUP")
# api_host_bak2 = os.environ.get("OPENAI_API_BASE_BACKUP2")
# gpt_model = "gpt-3.5-turbo"

import timeout_decorator  # pip install timeout-decorator
from retrying import retry
import warnings
import platform

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


# gpt_model = "gpt-3.5-turbo-16k"

# TODO 16k有很多时候的结果是需要继续的，当前没有做“继续”指令
# @timeout_and_retry(timeout=BAOSTOCK_TIMEOUT, wait_fixed=BAOSTOCK_WAIT_INTERVAL,stop_max_attempt_number=BAOSTOCK_RETRY,retry_on_exception=BaostockUtils.exception)
# @retry(wait_fixed=BAOSTOCK_WAIT_INTERVAL, stop_max_attempt_number=BAOSTOCK_RETRY,
#        retry_on_exception=BaostockUtils.exception)
# @timeout_decorator.timeout(BAOSTOCK_TIMEOUT,use_signals=False)  # 有问题，signal only works in main thread of the main interpreter
def get_openai_data(query=None, prompt=None, model='gpt-3.5-turbo',temperature=0.0):
    content = None
    # url = f'{api_host}/chat/completions'
    url = f'{config.OPENAI_API_HOST_USE}/chat/completions'
    headers = {'Authorization': f'Bearer {config.OPENAI_API_KEY}',
               'Content-Type': 'application/json'}

    real_query = prompt.replace("{query_str}", query) if prompt is not None else query
    data = {
        "model": model,
        "temperature": temperature,
        "messages": [{"role": "user", "content": real_query}]
    }
    slogger.info(f"get_openai_data: model:{model}")
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=300)  # 不然服务器会卡死
        slogger.info(response)
        slogger.info(f"url:{url}, query:{query}")
        slogger.info(f"real_query:{real_query}")
        slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
        if response.status_code == 200:
            if "That model is currently overloaded with other requests" in response.text:
                slogger.info(f"openai overloaded, get_openai_data retrying:{url}")
                time.sleep(3)
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=300)
                slogger.info(response)
                slogger.info(f"query:{query}")
                slogger.info(f"real_query:{real_query}")
                slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
            json_dict = response.json()  # 解析JSON
            slogger.info(f"json_dict:{json_dict}")
            # 从JSON字符串中提取内容字段
            content = json_dict['choices'][0]['message']['content']  # 获取指定字段
            slogger.info(f"content:{content}")
        else:
            slogger.info("请求失败")
    except Exception as e:
        traceback.print_exc()
        slogger.info(f"error:{e}")
    return content
    # 处理响应结果


@retry(wait_fixed=BAOSTOCK_WAIT_INTERVAL, stop_max_attempt_number=BAOSTOCK_RETRY,
       retry_on_exception=BaostockUtils.exception)
# @timeout_decorator.timeout(BAOSTOCK_TIMEOUT,use_signals=False)  # 有问题，signal only works in main thread of the main interpreter
def get_openai_data_davinci(query=None, prompt=None, model='text-davinci-003'):
    content = None
    # url = f'{api_host}/chat/completions'
    url = f'{config.OPENAI_API_HOST_USE}/completions'
    headers = {'Authorization': f'Bearer {config.OPENAI_API_KEY}',
               'Content-Type': 'application/json'}

    real_query = prompt.replace("{query_str}", query)
    data = {
        "model": model,
        "prompt": real_query,
        "temperature": 0
    }
    slogger.info(f"get_openai_data: model:{model}")
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=300)  # 不然服务器会卡死
        slogger.info(response)
        slogger.info(f"url:{url}, query:{query}")
        slogger.info(f"real_query:{real_query}")
        slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
        if response.status_code == 200:
            if "That model is currently overloaded with other requests" in response.text:
                slogger.info(f"openai overloaded, get_openai_data retrying:{url}")
                time.sleep(3)
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=300)
                slogger.info(response)
                slogger.info(f"query:{query}")
                slogger.info(f"real_query:{real_query}")
                slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
            json_dict = response.json()  # 解析JSON
            slogger.info(f"json_dict:{json_dict}")
            # 从JSON字符串中提取内容字段
            content = json_dict['choices'][0]['text']  # 获取指定字段
            slogger.info(f"content:{content}")
        else:
            slogger.info("请求失败")
    except Exception as e:
        traceback.print_exc()
        slogger.info(f"error:{e}")
    return content
    # 处理响应结果


def chat_translate(text, target_lang='English'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.OPENAI_API_KEY}'
    }
    url = f"{config.OPENAI_API_HOST_USE}/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{
            'role': 'system',
            'content': 'You are a translator assistant.'
        }, {
            "role":
                "user",
            "content":
                f"Translate the following text into {target_lang} language. Retain the original format. Return only the translation (without original text) and nothing else:\n{text}"
        }]
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    slogger.info(response.text)
    return response.text


def get_similarity(text1, text2, local_embedding=True):
    if local_embedding:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/distiluse-base-multilingual-cased-v2")
        embed_model = LangchainEmbedding(embeddings)
    else:
        # embeddings = OpenAIEmbeddings()
        embed_model = OpenAIEmbedding()  # embeddings = OpenAIEmbeddings(openai_api_key="xxxxxxx", chunk_size=1500)
    # text1 = "今天天气不错，出去玩"
    # text2 = "今天天气很好，不去玩了"
    t1 = embed_model.get_query_embedding(text1)
    t2 = embed_model.get_query_embedding(text2)
    res = embed_model.similarity(t1, t2)
    return res


def remove_duplicates(texts: List[str]) -> List[str]:
    slogger.info(f"remove_duplicates before:{len(texts)}")
    # 简单去重
    texts = list(set(texts))
    if len(texts) < 2:
        return texts
    # 相似度去重
    threshold = 0.9  # 相似度阈值
    # 相似且长度最长的留下
    _texts = copy.deepcopy(texts)
    for i in range(len(texts)):
        for j in range(len(texts)):
            try:
                if i == j:  # 自己不和自己比
                    continue
                score = get_similarity(texts[i], texts[j])
                if score >= threshold:
                    # 相似，则留下长的
                    if len(texts[i]) > len(texts[j]):
                        _texts.remove(texts[j])
                        slogger.info(f"remove_duplicates removed:{texts[j]}")
                    else:
                        _texts.remove(texts[i])
                        slogger.info(f"remove_duplicates removed:{texts[i]}")
            except Exception as e:
                slogger.error(f"remove_duplicates error:{e}")
                slogger.info(f"remove_duplicates texts:{_texts}")
    slogger.info(f"remove_duplicates after:{len(_texts)}")
    return _texts

# 不靠谱，很多对的也判错了
def llm_prune(query,bulleted_str):
    prompt = prompts.PRUNE_PROMPT.replace("{query_str}", query).replace("{bulleted_str}", bulleted_str)
    res = None
    try:
        result = get_openai_data(query=prompt, prompt=None, model='gpt-3.5-turbo-16k',temperature=0.7)
        result = json.loads(result)
        res = list(result.keys())
    except Exception as e:
        slogger.error(f"llm_prune:{e}")
    return res
import json
import os
import time
import traceback
import sqlite3

import requests
import prompts
from log_tool import slogger
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
api_host = os.environ.get("OPENAI_API_BASE")
api_host_bak = os.environ.get("OPENAI_API_BASE_BACKUP")
api_host_bak2 = os.environ.get("OPENAI_API_BASE_BACKUP2")
gpt_model = "gpt-3.5-turbo"

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


# @timeout_and_retry(timeout=BAOSTOCK_TIMEOUT, wait_fixed=BAOSTOCK_WAIT_INTERVAL,stop_max_attempt_number=BAOSTOCK_RETRY,retry_on_exception=BaostockUtils.exception)
@retry(wait_fixed=BAOSTOCK_WAIT_INTERVAL, stop_max_attempt_number=BAOSTOCK_RETRY,
       retry_on_exception=BaostockUtils.exception)
# @timeout_decorator.timeout(BAOSTOCK_TIMEOUT,use_signals=False)  # 有问题，signal only works in main thread of the main interpreter
def get_data(query=None, prompt=None, model='gpt-3.5-turbo'):
    content = None
    # url = f'{api_host}/chat/completions'
    url = f'{api_host_bak}/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}',
               'Content-Type': 'application/json'}

    real_query = prompt.replace("{query_str}", query)
    data = {
        "model": model,
        "messages": [{"role": "user", "content": real_query}]
    }
    slogger.info(f"get_data: model:{model}")
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers,timeout=300)   # 不然服务器会卡死
        slogger.info(response)
        slogger.info(f"url:{url}, query:{query}")
        slogger.info(f"real_query:{real_query}")
        slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
        if response.status_code == 200:
            if "That model is currently overloaded with other requests" in response.text:
                slogger.info(f"openai overloaded, get_data retrying:{url}")
                time.sleep(3)
                response = requests.post(url, data=json.dumps(data), headers=headers,timeout=300)
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


def chat_translate(text, target_lang='English'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    url = f"{api_host}/chat/completions"
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

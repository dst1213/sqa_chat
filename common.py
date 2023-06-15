import json
import os
import traceback
import sqlite3

import requests
import prompts
from log_tool import slogger
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
api_host = os.environ.get("OPENAI_API_BASE")
gpt_model = "gpt-3.5-turbo"
# gpt_model = "gpt-3.5-turbo-16k"


def get_data(query=None, prompt=None, model='gpt-3.5-turbo'):
    content = None
    url = f'{api_host}/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}',
               'Content-Type': 'application/json'}

    real_query = prompt.replace("{query_str}", query)
    data = {
        "model": model,
        "messages": [{"role": "user", "content": real_query}]
    }
    slogger.info(f"get_data: model:{model}")
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        slogger.info(response)
        slogger.info(f"query:{query}")
        slogger.info(f"real_query:{real_query}")
        slogger.info(f"response.status_code:{response.status_code}, response.text:{response.text}")
        if response.status_code == 200:
            json_dict = response.json()  # 解析JSON
            slogger.info(f"json_dict:{json_dict}")
            # 从JSON字符串中提取内容字段
            content = json_dict['choices'][0]['message']['content']  # 获取指定字段
            slogger.info(content)
        else:
            slogger.info("请求失败")
    except Exception as e:
        traceback.print_exc()
        slogger.info(f"error:{e}")
    return content
    # 处理响应结果


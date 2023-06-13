import json
import traceback

import requests
import prompt_templates
from log_tool import slogger
from dotenv import load_dotenv

load_dotenv()


def get_data(query=None, prompt=None):
    content = None
    url = 'https://gpt-api.putaojie.top/v1/chat/completions'
    headers = {'Authorization': 'Bearer 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',
               'Content-Type': 'application/json'}

    real_query = prompt.replace("{query_str}", query)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": real_query}]
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        slogger.info(response)
        slogger.info(f"query:{query}")
        slogger.info(f"real_query:{real_query}")

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

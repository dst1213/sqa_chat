import json
import traceback

import requests
import prompt_templates
from dotenv import load_dotenv

load_dotenv()


def get_data(query=None):
    content = None
    url = 'https://gpt-api.putaojie.top/v1/chat/completions'
    headers = {'Authorization': 'Bearer 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',
               'Content-Type': 'application/json'}
    my_prompt = prompt_templates.INTENT_TO_TABLE_PROMPTS
    real_query = my_prompt.replace("{query_str}", query)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": real_query}]
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response)
        print(f"query:{query}")
        print(f"real_query:{real_query}")

        if response.status_code == 200:
            json_dict = response.json()  # 解析JSON
            print(f"json_dict:{json_dict}")
            # 从JSON字符串中提取内容字段
            content = json_dict['choices'][0]['message']['content']  # 获取指定字段
            print(content)
        else:
            print("请求失败")
    except Exception as e:
        traceback.print_exc()
        print(f"error:{e}")
    return content
    # 处理响应结果

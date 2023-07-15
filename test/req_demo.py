import time
from concurrent.futures import ThreadPoolExecutor

import requests

def send_request(api_url, params):
    try:
        response = requests.post(api_url, data=params,timeout=300)
        response.raise_for_status()  # 如果响应状态码不是 200，就抛出异常
        json_response = response.json()
        if 'error' in json_response['data']:  # 如果返回的结果中包含错误信息，也抛出异常
            raise Exception(json_response['data']['error'])
        return json_response
    except Exception as e:
        print(f"Failed to get response from {api_url}, Error: {e}")
        return None

params = {
    "user": "tom_123",
    "domain": "all",
    "lang": "简体中文",
    # "query":"Alice Shaw的所有临床研究"
    "query":"alice shaw的邮箱"
    # "query": "口腔炎能参加NCT00080002吗"
}

sqa_url = "http://localhost:5000/sqa"  # 你需要替换成实际的 URL
dbqa_url = "http://localhost:5001/dbqa"  # 你需要替换成实际的 URL

# response = send_request(sqa_url, params)
# if response is None:
#     response = send_request(dbqa_url, params)
#
# print(response)
with ThreadPoolExecutor(max_workers=2) as executor:
    future_sqa = executor.submit(send_request, sqa_url, params)
    time.sleep(1)
    future_dbqa = executor.submit(send_request, dbqa_url, params)

response_sqa = future_sqa.result()
response_dbqa = future_dbqa.result()

print("==============")
if response_sqa is not None:
    print(response_sqa)
if response_sqa is not None:
    print("更多>>>")
    print(response_dbqa)
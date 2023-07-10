import time
import traceback

import requests

import requests

base_url = "http://127.0.0.1:5000/crawl"

def get_json(url):
    payload = {'user': 'tom_123','url': url}

    try:
        response = requests.post(base_url, data=payload,timeout=900)

        print(response.text)
        data = response.json()
        with open(f"data/{data['data']['name']}.txt",'w',encoding='utf8') as f:
            f.write(url+'\n')
            f.write(response.text)
    except Exception as e:
        traceback.print_exc()
        print(e)

if __name__== "__main__":
    with open("data/urls.txt","r",encoding="utf8") as f:
        urls = f.readlines()
    for url in urls:
        print(f"start url:{url.strip()}")
        get_json(url.strip())
        time.sleep(21)
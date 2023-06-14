import asyncio
import json
import logging
import os
import tempfile
import traceback

from bs4 import BeautifulSoup
import requests
from flask import Flask, request, Response, render_template, stream_with_context, jsonify
import websockets

import prompts
from common import get_data
from handlers import get_table
from log_tool import slogger

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return {"status": "ok"}


@app.route('/crawl', methods=['POST'])
def html_handler():
    user = request.form.get("user", "")
    url = request.form.get("url", "")
    response = requests.get(url, verify=False)  # 解决中肿网页Https无法爬取
    soup = BeautifulSoup(response.content, 'html.parser')
    # 从HTML中提取出文本内容并去除换行、空格等字符
    text = soup.get_text().replace('\n', '').replace('\r', '').replace('\t', '').strip()
    slogger.info(f"type:{type(text)},text:{text}")

    # Pass the SpooledTemporaryFile to UploadFile
    prompt = prompts.FIELD_EXTRACTOR_TEMPLATE
    result = get_data(text,prompt,model='gpt-3.5-turbo-16k')
    slogger.info(f"result:{result}")
    temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}.txt")
    slogger.info(f"temp_file_path:{temp_file_path}")
    # 即使抽取失败，不影响索引构建，但是可能影响名片字段的入库 TODO
    with open(temp_file_path, 'w', encoding='utf8') as temp_file:
        if result:
            temp_file.write(str(result))
        else:
            temp_file.write(str(text))


    return {"data": "success"}


@app.route('/text', methods=['POST'])
def text_handler():
    user = request.form.get("user", "")
    text = request.form.get("text", "")
    slogger.info(f"len text:{len(text)}，txt:{text}")
    slogger.info("超出4096的部分将截断！！！")  # TODO 按\n截取，4k以内最长的\n，分段解析再合并
    text = text[:4000]
    slogger.info(text)

    temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}.txt")
    slogger.info(f"temp_file_path:{temp_file_path}")
    with open(temp_file_path, 'w', encoding='utf8') as temp_file:
        temp_file.write(str(text))

    # 构建索引
    construct_index(api_key, file_src=[temp_file], user_id=user, whole_update=True, max_input_size=4096,
                    num_outputs=5,
                    max_chunk_overlap=20, chunk_size_limit=600,
                    embedding_limit=None, separator=" ", )
    return {"data": "success"}


@app.route('/sqa', methods=['POST'])
def sqa_handler():
    user = request.form.get("user", "test")
    domain = request.form.get("domain", "faq")
    lang = request.form.get("lang", "简体中文")  # lang字面量必须和query的语言一致才可以
    query = request.form.get("query", "hello")
    slogger.info(f"user:{user}, domain:{domain}, lang:{lang}, query:{query}")
    try:
        db_chain = get_table(table=domain, query=query, lang=lang)
        res = db_chain.run(query)
    except Exception as e:
        traceback.print_exc()
        res = {'error': str(e)}
    return {'data': res}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


import asyncio
import json
import logging
import os
import random
import tempfile
import traceback

from bs4 import BeautifulSoup
import requests
from flask import Flask, request, Response, render_template, stream_with_context, jsonify
import websockets

import prompts
from llm_tools import get_openai_data, chat_translate
from db_models import write_doctor_table
from handlers import get_table
from log_tools import slogger

from dotenv import load_dotenv

from utils import web_text_extractor, get_html, get_html_by_sn, get_html_by_pw, get_html_by_file

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
    try:
        # 爬虫
        # soup,text,raw_text = get_html(url)  # requests
        soup,text,raw_text = get_html_by_sn(url)  # selenium, list-cooper
        # soup, text, raw_text = get_html_by_pw(url)  # playwright
        # soup, text, raw_text = get_html_by_file("test/data/ru-en.txt")  # 本地文件
        # 结构化抽取
        # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L1
        # result = get_openai_data(text, prompt, model='gpt-3.5-turbo')  # gpt-3.5-turbo-16k
        repeat = 0
        # TODO 等解决了16k的“继续"指令后再改txt为json，txt的多个分块问题多，先截断了
        result = web_text_extractor(text[:45000], raw_text=raw_text,limit=50000, repeat=repeat, out_type='txt', model_type='gpt-3.5-turbo-16k', url=url)  # default repeat=0  # 15000比较好
        slogger.info(f"repeat:{repeat},result:{result}")
        name_suffix = random.randint(1, 10000)
        temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}_{name_suffix}.txt")
        slogger.info(f"temp_file_path:{temp_file_path}")
        # 即使抽取失败，不影响索引构建，但是可能影响名片字段的入库 TODO
        with open(temp_file_path, 'w', encoding='utf8') as temp_file:
            if result:
                temp_file.write(str(result))
            else:
                temp_file.write(str(text))

        data = result
        # data = json.loads(result) if isinstance(result,str) else result
        # # 字段入库
        # write_doctor_table(table_info=data, table_name='doctor', db_name=user, class_name='Doctor', fields_info=None,
        #                    drop_first=True, back_first=True)
    except Exception as e:
        slogger.error(f"html_handler error:{e}")
        traceback.print_exc()
        return {"status":"failure","data":{}}
    return {"status": "success", "data": data}


@app.route('/text', methods=['POST'])
def text_handler():
    user = request.form.get("user", "")
    text = request.form.get("text", "")
    # slogger.info(f"len text:{len(text)}，txt:{text}")
    # slogger.info("超出4096的部分将截断！！！")  # TODO 按\n截取，4k以内最长的\n，分段解析再合并
    # text = text[:4000]
    slogger.info(text)

    temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}.txt")
    slogger.info(f"temp_file_path:{temp_file_path}")
    with open(temp_file_path, 'w', encoding='utf8') as temp_file:
        temp_file.write(str(text))

    # 结构化抽取
    # prompt = prompts.FIELD_EXTRACTOR_TEMPLATE_L1
    # result = get_openai_data(text, prompt, model='gpt-3.5-turbo')  # gpt-3.5-turbo-16k
    repeat = 0
    result = web_text_extractor(text, limit=2000, repeat=repeat, model_type='gpt-3.5-turbo')
    slogger.info(f"result:{result}")

    data = json.loads(result)
    # 字段入库
    write_doctor_table(table_info=data, table_name='doctor', db_name=user, class_name='Doctor', fields_info=None,
                       drop_first=True, back_first=True)

    return {"status": "success", "data": data}


@app.route('/sqa', methods=['POST'])
def sqa_handler():
    user = request.form.get("user", "")
    domain = request.form.get("domain", "faq")
    lang = request.form.get("lang", "简体中文")  # lang字面量必须和query的语言一致才可以
    query = request.form.get("query", "hello")
    slogger.info(f"user:{user}, domain:{domain}, lang:{lang}, query:{query}")
    try:
        db_chain = get_table(user, table=domain, query=query, lang=lang)
        res = db_chain.run(query)
    except Exception as e:
        traceback.print_exc()
        res = {'error': str(e)}
    return {'data': res}


@app.route('/trans', methods=['POST'])
def chatgpt_trans():
    user = request.form.get("user", "test")
    target_lang = request.form.get("target_lang", "English")  # lang字面量必须和query的语言一致才可以
    query = request.form.get("query", "你好")
    slogger.info(f"user:{user},  target_lang:{target_lang}, query:{query}")
    try:
        res = chat_translate(query, target_lang=target_lang)
    except Exception as e:
        traceback.print_exc()
        res = {'error': str(e)}
    return {'data': res}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

# ----------------------------------------------------------------------------------
import asyncio
import json
import logging
import os
import tempfile

from bs4 import BeautifulSoup
import requests
from flask import Flask, request, Response, render_template, stream_with_context, jsonify
import websockets

def echo():
    pass

# websocket
async def main():
    # start a websocket server
    async with websockets.serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever


# sse

from werkzeug.utils import secure_filename

app = Flask(__name__)

# index
# app.config内的配置名均为固定搭配
# 储存上传的文件的地方
app.config['UPLOAD_FOLDER'] = 'uploads/'
# 允许的文件类型的集合
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sh', 'json'])
# 上传文件限制为最大 16MB，如果请求传输一个更大的文件， Flask 会抛出一个 RequestEntityTooLarge 异常。
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

api_key = os.environ.get("OPENAI_API_KEY")


def allowed_file(filename):
    """
    判断传入的文件后缀是否合规。不合规返回False
    :param filename:
    :return: True or False
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload():
    # postman：POST -> Body -> form-data -> KEY=files
    uploaded_files = request.files.getlist("files")
    user_id = request.form.get("user", "")
    logging.info(f"uploaded_files:{uploaded_files}")
    file_paths = [x.name for x in uploaded_files]
    logging.info(f"file_paths:{file_paths}")
    filenames = []
    error_filenames = []
    allow_files = []
    # gradio的文件在临时文件夹， C:\Users\putao\AppData\Local\Temp\b8d6a955aeb1181141ddd8b3210e9736303a9287\yyl.txt
    # 此处后边也要改成tempfile模式？？？ TODO
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            logging.info(f"filename.:{file.filename}")
            # filename = secure_filename(file.filename)  # NND，对中文不友好，导致文件名丢失！！！
            filename = file.filename
            logging.info(f"filename:{filename}")
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_filename)
            filenames.append(filename)
            # 组装file参数，否则是错误的，导致只有最后一份有数据 !!!
            file.name = full_filename
            logging.info(f"file.name:{file.name}")

            allow_files.append(file)  # TODO 可以直接返回str（allow_files)，避免等待太久，增加训练接口
        else:  # 文件后缀不符合类型或者文件太大
            error_filenames.append(file.filename)
    # 构建索引
    construct_index(api_key, file_src=allow_files, user_id=user_id, whole_update=True, max_input_size=4096,
                    num_outputs=5,
                    max_chunk_overlap=20, chunk_size_limit=600,
                    embedding_limit=None, separator=" ", )

    if error_filenames:  # 有文件上传失败的情况
        result = {
            'code': 200,
            'result': 'failure',
            'message': ",".join(error_filenames)
        }
        return result
    else:
        result = {
            'code': 200,
            'result': 'success',
            'message': ''
        }
        return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query')
def query():
    text = request.args.get('content', "你好")
    user = request.args.get('user', '')
    logging.info(text)
    res = chatbot_data(text, user)
    return res


@app.route('/chatbot_data')
def chatbot_data(message="写个故事，50字以内", user=''):
    logging.info('chatbot_data-' * 5)

    def get_predict_data(message, user=''):
        client, message, chatbot, stream = chat(message)
        force_index = True  # 强制使用索引 TODO
        add_refs = False  # 强制不附带参考出处 TODO
        reply_language = "跟随问题语言（不稳定）"  # 自动跟随  TODO
        for i in client.predict(inputs=message, chatbot=chatbot, stream=stream, force_index=force_index,
                                base_index='index', user_id=user, add_refs=add_refs, reply_language=reply_language):
            logging.info(i)
            d = i[0][0][-1]
            logging.info(d)
            json_data = json.dumps(
                {'time': 0, 'value': d})
            # json_data = json.dumps(
            #     {'time': a, 'value': random.random() * 100})
            # 1 SSE 返回格式是json字符串，要使用yield返回，字符串后面一定要跟随 \n\n
            yield f"data:{json_data}\n\n"
            # time.sleep(1)  # 1s 发送一次

    # 2 stream_with_context 设置SSE连接函数，mimetype="text/event-stream" 是设置SSE返回格式
    response = Response(stream_with_context(get_predict_data(message, user)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.route('/crawl', methods=['POST'])
def html_handler():
    user = request.form.get("user", "")
    url = request.form.get("url", "")
    response = requests.get(url, verify=False)  # 解决中肿网页Https无法爬取
    soup = BeautifulSoup(response.content, 'html.parser')
    # 从HTML中提取出文本内容并去除换行、空格等字符
    text = soup.get_text().replace('\n', '').replace('\r', '').replace('\t', '').strip()
    logging.info(f"type:{type(text)},text:{text}")

    def get_data(txt=None):
        content = ""
        try:
            logging.info(f"len txt:{len(txt)}，txt:{txt}")
            logging.info("超出4096的部分将截断！！！")  # TODO 按\n截取，4k以内最长的\n，分段解析再合并
            txt = txt[:4000]
            url = 'https://openai.putaojie.top/v1/chat/completions'
            headers = {'Authorization': f'Bearer {api_key}',
                       'Content-Type': 'application/json'}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user",
                              "content": "Notice: If doctor or hospital not in the context, skip this one 假如你是数据工程师，请把如下个人信息按照JSON的格式整理给我：（参考字段：行医，门诊时间，综合评价，资质认证状态，基本信息，简介，姓名，医院/机构，专长，职务，职称，学术兼职，地区，邮箱，手机，昕康ID/XK_ID，履历，教育经历，工作经历，研究，研究方向/临床研究，课题/基金，发表，发表文章，出版著作，专利和软著，执笔共识，成就，荣誉获奖）Return only the translation and nothing else:\n" + txt}]
            }

            response = requests.post(url, data=json.dumps(data), headers=headers)
            logging.info(response.status_code)
            # 处理响应结果
            if response.status_code == 200:
                json_dict = response.json()  # 解析JSON
                # 从JSON字符串中提取内容字段
                content = json.loads(json_dict['choices'][0]['message']['content'])  # 获取指定字段
                logging.info(f"content:{content}")
                # with open(f'doc/{i}.json', 'w', encoding='utf-8') as f:
                #     f.write(json.dumps(content, ensure_ascii=False))
            else:
                logging.info("请求失败")
        except Exception as e:
            logging.error(f"get_data error:{e}")
        return content

    # Pass the SpooledTemporaryFile to UploadFile
    result = get_data(text)
    logging.info(f"result:{result}")
    temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}.txt")
    logging.info(f"temp_file_path:{temp_file_path}")
    # 即使抽取失败，不影响索引构建，但是可能影响名片字段的入库 TODO
    with open(temp_file_path, 'w', encoding='utf8') as temp_file:
        if result:
            temp_file.write(str(result))
        else:
            temp_file.write(str(text))

    # 构建索引
    construct_index(api_key, file_src=[temp_file], user_id=user, whole_update=True, max_input_size=4096,
                    num_outputs=5,
                    max_chunk_overlap=20, chunk_size_limit=600,
                    embedding_limit=None, separator=" ", )
    return {"data": "success"}


@app.route('/text', methods=['POST'])
def text_handler():
    user = request.form.get("user", "")
    text = request.form.get("text", "")
    logging.info(f"len text:{len(text)}，txt:{text}")
    logging.info("超出4096的部分将截断！！！")  # TODO 按\n截取，4k以内最长的\n，分段解析再合并
    text = text[:4000]
    logging.info(text)

    temp_file_path = os.path.join(tempfile.gettempdir(), f"{user}.txt")
    logging.info(f"temp_file_path:{temp_file_path}")
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
    user = request.form.get("user", "")
    query = request.form.get("query", "")

    import json

    from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
    db = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
    llm = OpenAI(temperature=0, verbose=True)
    from langchain.prompts.prompt import PromptTemplate

    _DEFAULT_TEMPLATE = """Given an input question, first translate to English,
    then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here", reply in Chinese language.

    Only use the following tables:

    {table_info}

    If someone asks for the table foobar, they really mean the employee table.

    Question: {input}"""
    PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
    )
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)
    res = db_chain.run(query)
    return {'data': res}


if __name__ == "__main__":
    deploy_mode = "sse"  # gr, hf, sse，ws，分别是gradio原版，huggingface部署模式，sse生产部署模式，websocket（当前只能非流式）

    if deploy_mode == "sse":
        app.run(debug=True, host="0.0.0.0", port=5000)

    elif deploy_mode == "ws":
        asyncio.run(main())

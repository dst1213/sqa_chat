import json
import traceback

import requests
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from dotenv import load_dotenv

load_dotenv()


# db = SQLDatabase.from_uri("sqlite:///med_db/doctor_0612.db", include_tables=['doctor'])
# db = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_all = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq','doctors'])
db_faq = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['faq'])
# db_ct = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_ct_demo = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial_demo', 'faq'])
# db_doctor = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['doctors','faq'])
db_doctor = SQLDatabase.from_uri("sqlite:///med_db/doctor.db", include_tables=['doctors'])
db_ct = SQLDatabase.from_uri("sqlite:///med_db/clinictrials.db", include_tables=['doctor'])

llm = OpenAI(temperature=0, verbose=True)



_DEFAULT_TEMPLATE = """Given an input question, first translate to English,
then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here", reply in Chinese language.

Only use the following tables:

{table_info}

Truncate SQLResult to less than 4000 tokens or length < 4000

Do not use Select * from

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

tables = {'all':db_all,'ct':db_ct,'doctor':db_doctor,'ct_demo':db_ct_demo}
tables2 = {'all':db_all,'clinical_trial':db_ct,'doctor':db_doctor,'ct_demo':db_ct_demo,'faq':db_faq}
all_tables = ['faq','doctor','clinical_trial']

def get_data(query=None):
    content = None
    url = 'https://gpt-api.putaojie.top/v1/chat/completions'
    headers = {'Authorization': 'Bearer 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',
               'Content-Type': 'application/json'}
    my_prompt = """
    根据以下三张表的表结构字段，判断这个问句（query）需要用到哪张表。
    问句:{query_str}

    [TableName:clinical_trial]
    id,First_Submitted_Date,First_Posted_Date,Last_Update_Posted_Date,Estimated_Study_Start_Date,Estimated_Primary_Completion_Date,Current_Primary_Outcome_Measures,Original_Primary_Outcome_Measures,Current_Secondary_Outcome_Measures,Original_Secondary_Outcome_Measures,Current_Other_Pre_specified_Outcome_Measures,Original_Other_Pre_specified_Outcome_Measures,Brief_Title,Official_Title,Brief_Summary,Detailed_Description,Study_Type,Study_Phase,Study_Design,Condition,Intervention,Study_Arms,Publications,Recruitment_Status,Estimated_Enrollment,Original_Estimated_Enrollment,Estimated_Study_Completion_Date,Estimated_Primary_Completion_Date1,Eligibility_Criteria,Gender,Ages,Accepts_Healthy_Volunteers,Contacts,Listed_Location_Countries,Removed_Location_Countries,NCT_Number,Other_Study_ID_Numbers,Has_Data_Monitoring_Committee,US_FDA_regulated_Product,IPD_Sharing_Statement,Current_Responsible_Party,Original_Responsible_Party,Current_Study_Sponsor,Original_Study_Sponsor,Collaborators,Investigators,PRS_Account,Verification_Date

    [TableName:doctor]
    _id,avatar,name,hospital,title,position,contact,phone,expertise,brief_intro,work_exp,edu_exp,consulting,publications,clinical_res,awards

    [TableName:faq]
    Frequently_Asked_Question,Answer

    Return only the table name and nothing else
    """
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

def clean_table_name(table_name):
    _table_name = 'faq' # table_name
    if table_name is None:
        return _table_name
    for t in all_tables:
        if t in table_name:
            _table_name = t
            break
    return _table_name

def get_table(table='ct',query=None):
    if table == 'auto':
        table_name = get_data(query)
        table_name = clean_table_name(table_name)
        db = tables2[table_name] if table_name in all_tables else tables2['faq']
    else:
        db = tables[table]
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, top_k=3)
    return db_chain


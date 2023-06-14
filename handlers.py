# coding:utf-8
import json
import logging
import traceback

import requests
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

import prompts
from common import *
from log_tool import slogger
from dotenv import load_dotenv

load_dotenv()

# db = SQLDatabase.from_uri("sqlite:///med_db/doctor_0612.db", include_tables=['doctor'])
# db = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
# db_all = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq', 'doctors'])
db_all = SQLDatabase.from_uri("sqlite:///med_db/doctor_tom.db", include_tables=['clinical_trial', 'faq_chinese', 'doctor_spanish','doctor'])
# db_faq = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['faq'])
db_faq = SQLDatabase.from_uri("sqlite:///med_db/doctor_tom.db", include_tables=['faq_chinese'])  # 2023年6月13日
db_faq_new = SQLDatabase.from_uri("sqlite:///med_db/faq_chinese_new.db", include_tables=['faq_chinese_new'])

# db_ct = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_ct_demo = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial_demo', 'faq'])
# db_doctor = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['doctors','faq'])
# db_doctor = SQLDatabase.from_uri("sqlite:///med_db/doctor.db", include_tables=['doctors'])  # 2023.06.12 doctor
# db_doctor = SQLDatabase.from_uri("sqlite:///med_db/doctor_tom.db", include_tables=['doctor'])  # 2023年6月13日
db_doctor = SQLDatabase.from_uri("sqlite:///med_db/doctor_tom.db", include_tables=['doctor_spanish'])  # 2023年6月14日
# db_ct = SQLDatabase.from_uri("sqlite:///med_db/clinicaltrials.db", include_tables=['doctor'])  # 2023.06.12 clinical_trial
db_ct = SQLDatabase.from_uri("sqlite:///med_db/doctor_tom.db", include_tables=['clinical_trial'])  # 2023年6月13日
db_pb = SQLDatabase.from_uri("sqlite:///med_db/pubmed2.db", include_tables=['pubmed'])  # 2023.06.12 clinical_trial
# db_user = SQLDatabase.from_uri("sqlite:///med_db/{user}.db")  # 2023.06.14 user db

# GPT - OpenAI API  https://platform.openai.com/docs/guides/gpt
llm = OpenAI(model_name="text-davinci-003", temperature=0, verbose=True)  # davinci旧模型
# llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",temperature=0, verbose=True)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0, verbose=True)

tables = {'all': db_all, 'ct': db_ct, 'doctor': db_doctor, 'ct_demo': db_ct_demo, 'pb': db_pb, 'faq':db_faq_new}
tables2 = {'all': db_all, 'clinical_trial': db_ct, 'doctor': db_doctor, 'ct_demo': db_ct_demo, 'faq': db_faq_new,
           'pubmed': db_pb}
all_tables = ['faq', 'doctor', 'clinical_trial']


def clean_table_name(table_name):
    _table_name = 'faq'  # table_name
    if table_name is None:
        return _table_name
    for t in all_tables:
        if t in table_name:
            _table_name = t
            break
    return _table_name


def get_table(user,table='ct', query=None, lang="简体中文"):
    if user:
        db_user = SQLDatabase.from_uri(f"sqlite:///med_db/{user}.db")  # 2023.06.14 user db
        tables2 = {"all":db_user,'faq':db_faq, 'doctor':db_user,'clinical_trial':db_user}
    if table == 'auto':
        prompt = prompts.INTENT_TO_TABLE_PROMPTS
        table_name = get_data(query, prompt=prompt)
        table_name = clean_table_name(table_name)
        slogger.info(f"table_name:{table_name}")
        db = tables2[table_name] if table_name in all_tables else tables2['faq']
    else:
        db = tables[table]
    sql_prompt = prompts.get_sql_lang_prompt(lang)
    slogger.info(f"sql_prompt:{sql_prompt}")
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=sql_prompt, verbose=True, top_k=3)
    return db_chain


def get_sim_query(query, prompt):
    prompt = prompts.SIMILAR_QUESTION_TEMPLATE
    sim_queris = get_data(query, prompt=prompt)

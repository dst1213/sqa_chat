import json
import traceback

import requests
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

import prompt_templates
from common import *
from dotenv import load_dotenv

load_dotenv()

# db = SQLDatabase.from_uri("sqlite:///med_db/doctor_0612.db", include_tables=['doctor'])
# db = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_all = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq', 'doctors'])
db_faq = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['faq'])
# db_ct = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_ct_demo = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial_demo', 'faq'])
# db_doctor = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['doctors','faq'])
db_doctor = SQLDatabase.from_uri("sqlite:///med_db/doctor.db", include_tables=['doctors'])  # 2023.06.12 doctor
db_ct = SQLDatabase.from_uri("sqlite:///med_db/clinictrials.db", include_tables=['doctor'])  # 2023.06.12 clinical_trial
db_pb = SQLDatabase.from_uri("sqlite:///med_db/pubmed2.db", include_tables=['pubmed'])  # 2023.06.12 clinical_trial

llm = OpenAI(temperature=0, verbose=True)

tables = {'all': db_all, 'ct': db_ct, 'doctor': db_doctor, 'ct_demo': db_ct_demo, 'pb': db_pb}
tables2 = {'all': db_all, 'clinical_trial': db_ct, 'doctor': db_doctor, 'ct_demo': db_ct_demo, 'faq': db_faq,
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


def get_table(table='ct', query=None):
    if table == 'auto':
        table_name = get_data(query)
        table_name = clean_table_name(table_name)
        db = tables2[table_name] if table_name in all_tables else tables2['faq']
    else:
        db = tables[table]
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=prompt_templates.SQL_PROMPT, verbose=True, top_k=3)
    return db_chain

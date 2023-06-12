from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from dotenv import load_dotenv

load_dotenv()


# db = SQLDatabase.from_uri("sqlite:///med_db/doctor_0612.db", include_tables=['doctor'])
# db = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_all = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq','doctors'])
db_ct = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial', 'faq'])
db_ct_demo = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['clinical_trial_demo', 'faq'])
db_doctor = SQLDatabase.from_uri("sqlite:///med_db/test.db", include_tables=['doctors','faq'])

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
def get_table(table='ct'):
    db = tables[table]
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, top_k=3)
    return db_chain


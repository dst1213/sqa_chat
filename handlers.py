from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from dotenv import load_dotenv

load_dotenv()

# db = SQLDatabase.from_uri("sqlite:///med_db/doctor_0612.db", include_tables=['clinical_trial', 'faq'])
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

Truncate SQLResult to less than 4000 tokens or length < 4000

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)
db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, top_k=3)
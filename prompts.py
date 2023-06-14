from langchain import PromptTemplate

FIELD_EXTRACTOR_TEMPLATE = """
    Notice: If doctor or hospital not in the context, skip this one 假如你是数据工程师，请把如下个人信息按照JSON的格式整理给我：（参考字段：行医，门诊时间，综合评价，资质认证状态，基本信息，简介，姓名，医院/机构，专长，职务，职称，学术兼职，地区，邮箱，手机，昕康ID/XK_ID，履历，教育经历，工作经历，研究，研究方向/临床研究，课题/基金，发表，发表文章，出版著作，专利和软著，执笔共识，成就，荣誉获奖）Return only the translation and nothing else:\n
    query:{query_str}
"""

FIELD_EXTRACTOR_TEMPLATE_L1 = """
    假如你是数据工程师，请把如下个人信息（query）按照JSON的格式整理给我：
    参考字段：专长，行医，门诊时间，综合评价，资质认证状态，基本信息，简介，姓名，医院机构，职务，职称，学术兼职，地区，邮箱，手机，昕康ID，履历，教育经历，工作经历，研究，研究方向和临床研究，课题和基金，发表，发表文章，出版著作，专利和软著，执笔共识，成就，荣誉获奖\n
    Notice: If doctor or hospital not in the context, skip this one\n
    JSON的格式：{"xxx":"xxx","xxx_xxx":"xxx"}，JSON的字段层级只能是一级，多个层级用"_"拼接，字段名和值都是字符串类型
    Return only the JSON and nothing else:\n
    query:{query_str}
"""

INTENT_TO_TABLE_PROMPTS = """
    根据以下三张表的表结构字段，判断这个问句（query）需要用到哪张表。
    问句:{query_str}
    
    [TableName:pubmed]
    name,email,affiliation,publication_status,article_id,article_references,article_title,journal_name,issn_type,issn_code,revision_date,publish_date,pubmed_id,article_abstract

    [TableName:clinical_trial]
    id,First_Submitted_Date,First_Posted_Date,Last_Update_Posted_Date,Estimated_Study_Start_Date,Estimated_Primary_Completion_Date,Current_Primary_Outcome_Measures,Original_Primary_Outcome_Measures,Current_Secondary_Outcome_Measures,Original_Secondary_Outcome_Measures,Current_Other_Pre_specified_Outcome_Measures,Original_Other_Pre_specified_Outcome_Measures,Brief_Title,Official_Title,Brief_Summary,Detailed_Description,Study_Type,Study_Phase,Study_Design,Condition,Intervention,Study_Arms,Publications,Recruitment_Status,Estimated_Enrollment,Original_Estimated_Enrollment,Estimated_Study_Completion_Date,Estimated_Primary_Completion_Date1,Eligibility_Criteria,Gender,Ages,Accepts_Healthy_Volunteers,Contacts,Listed_Location_Countries,Removed_Location_Countries,NCT_Number,Other_Study_ID_Numbers,Has_Data_Monitoring_Committee,US_FDA_regulated_Product,IPD_Sharing_Statement,Current_Responsible_Party,Original_Responsible_Party,Current_Study_Sponsor,Original_Study_Sponsor,Collaborators,Investigators,PRS_Account,Verification_Date

    [TableName:doctor]
    _id,avatar,name,hospital,title,position,contact,phone,expertise,brief_intro,work_exp,edu_exp,consulting,publications,clinical_res,awards

    [TableName:faq]
    Frequently_Asked_Question,Answer

    Return only the table name and nothing else
    """

SQL_LLM_TEMPLATE = """Given an input question, first translate to English,
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

SQL_LANG_TEMPLATE = """Given an input question, first translate to English,
    then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"
    
    reply in __lang_str__ language

    Only use the following tables:

    {table_info}

    Truncate SQLResult to less than 4000 tokens or length < 4000

    Do not use Select * from

    Question: {input}"""

SQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=SQL_LLM_TEMPLATE
)

def get_sql_lang_prompt(lang='Chinese'):
    sql_templ = SQL_LANG_TEMPLATE.replace("__lang_str__",lang)
    SQL_LANG_PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=sql_templ
    )
    return SQL_LANG_PROMPT

SIMILAR_QUESTION_TEMPLATE = """
假如你是自然语言处理工程师，
扩写以下问句（question）的相似问句，根据问句意图，可以使用如增加辅助词、同义词替换、口语化、表述形式变换等技巧来实现，
扩写10个，按JSONL格式回答：{"query":xxx}，Return only the JSON data and nothing else。

Question:{query_str}
"""

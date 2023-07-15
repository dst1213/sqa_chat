from langchain import PromptTemplate

import config

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

FIELD_EXTRACTOR_TEMPLATE_L2 = """
    假如你是数据工程师，请把如下个人信息（query）按照JSON的格式整理给我：
    参考字段：姓名(同义词：name)，医院机构（同义词：诊所，药厂，公司，hospital， clinic），科室（同义词：部门，department），职务（同义词：职位，position），职称（同义词：title），电话（同义词：contact，phone，mobile），邮箱（同义词：email，电邮），位置（同义词：地址，城市，location, office location），个人介绍（同义词：自我介绍，专家介绍，简介，about me，introduce），专长：（同义词：擅长，specialty，expertise），出诊时间（同义词：出诊信息，visit time，visit hours），资格证书（同义词：qualification），适用医保（同义词：医疗保险，医保，insurance），学术兼职（同义词：part-time，academic），工作经历（同义词：work experience，career），学习经历（同义词：学历，education），文献著作（同义词：出版、论文，publications），临床研究（同义词：研究，Clinical trial），荣誉成就（同义词：honor，achievement），服务语言（同义词：service language，language）\n
    Notice: If doctor or hospital not in the context, skip this one\n
    JSON的格式：{"xxx":"xxx","xxx_xxx":"xxx"}，JSON的字段层级只能是一级，多个层级用"_"拼接，字段名是字符串类型，字段值用list[]形式放入多个值
    Return only the JSON and nothing else:\n
    query:{query_str}
"""

FIELD_EXTRACTOR_TEMPLATE_L3 = """
    假如你是数据工程师，请把如下文本（context）按照JSON的格式整理给我：
    参考字段：姓名(同义词：name)，医院机构（同义词：诊所，药厂，公司，hospital，clinic），科室（同义词：部门，department），职务（同义词：职位，position），职称（同义词：title），电话（同义词：contact，phone，mobile），邮箱（同义词：email，电邮），位置（同义词：地址，城市，location, office location），个人介绍（同义词：自我介绍，专家介绍，简介，about me，introduce），专长：（同义词：擅长，specialty，expertise, interests），出诊时间（同义词：出诊信息，visit time，visit hours），资格证书（同义词：qualification），适用医保（同义词：医疗保险，医保，insurance），学术兼职（同义词：part-time，academic），工作经历（同义词：work experience，career，short bio），学习经历（同义词：学历，education），文献著作（同义词：出版，论文，publications，pubmed，pmid，pmcid），临床研究（同义词：研究，clinical trials），荣誉成就（同义词：honor，achievement），服务语言（同义词：service language，language），接诊对象（同义词：treats）\n
    JSON的格式：{"xxx":"xxx","xxx_xxx":"xxx"}，JSON的字段层级只能是一级，多个层级用"_"拼接，字段名是字符串类型，字段值用list[]形式放入多个值
    Return only the valid JSON and nothing else:\n
    ----------context:\n
    {query_str}
    ----------
"""

FIELD_EXTRACTOR_TEMPLATE_L4 = """
    假如你是数据工程师，请把如下文本（query）结构化整理给我（非JSON），只给我存在值的字段：
    参考字段：姓名(同义词：name)，医院机构（同义词：诊所，药厂，公司，hospital， clinic），科室（同义词：部门，department），职务（同义词：职位，position），职称（同义词：title），电话（同义词：contact，phone，mobile），邮箱（同义词：email，电邮），位置（同义词：地址，城市，location, office location），个人介绍（同义词：自我介绍，专家介绍，简介，about me，introduce），专长：（同义词：擅长，specialty，expertise），出诊时间（同义词：出诊信息，visit time，visit hours），资格证书（同义词：qualification），适用医保（同义词：医疗保险，医保，insurance），学术兼职（同义词：part-time，academic），工作经历（同义词：work experience，career），学习经历（同义词：学历，education），文献著作（同义词：出版，论文，publications，pubmed，pmid），临床研究（同义词：研究，Clinical trial），荣誉成就（同义词：honor，achievement），服务语言（同义词：service language，language）\n
    Return only the structured data and nothing else:\n
    query:{query_str}
"""
INTENT_TO_TABLE_PROMPTS_V2 = """
    根据以下7张表的表结构字段，判断这个问句（query）需要用到哪张表。
    问句:{query_str}
    
    [TableName:doctor]
    name,english_name,email,sex,title,position,contact,biography,expertise,visit_time,qualification,insurance,language
    其中contact,position,visit_time,qualification的值是json，具体如下：
    contact包含子字段：location,phone,email,fax
    position包含子字段：insitution,department,position
    visit_time包含子字段：visit_info,visit_location,visit_time
    qualification包含子字段：certification,fellowship,npi

    [TableName:achievements]
    type,info,time
    其中type的值包括：honor,achievement,awards，而info是具体内容

    [TableName:personal_experience]
    type,info,start_time,end_time
    其中type的值包括：career,education,part_time，而career和work experience是同义词，part_time是学术兼职的意思

    [TableName:clinical_trials_detail]
    nct_no,brief_title

    [TableName:pubmed_detail]
    pid,title,authors,cit,type
    其中type的值包括：pmid,pmcid，是pubmed文章的编号，共2种，而cit是引用信息

    [TableName:publications]
    type,info,time
    其中type的值包括：publications,pubmed,articles，而pubmed是一类文献，publications是文献和书籍的统称，articles是论文

    [TableName:medical_research]
    type,info,time
    其中type的值包括clinical_trials,research_interest,research_project，clinical_trials或者clinical trial是临床研究

    Return only the table name and nothing else
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

SQL_LLM_TEMPLATE_WITH_LIMIT = """Given an input question, first translate to English,
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

SQL_LLM_TEMPLATE_NO_LIMIT = """Given an input question, first translate to English,
    then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here", reply in Chinese language.

    Only use the following tables:

    {table_info}


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

SQL_LANG_TEMPLATE_NO_LIMIT = """Given an input question, first translate to English,
    then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    reply in __lang_str__ language

    Only use the following tables:

    {table_info}


    Do not use Select * from

    Question: {input}"""

SQL_LANG_TEMPLATE_NO_LIMIT_SYNONYMS = """Given an input question, first translate to English,
    then create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    reply in __lang_str__ language

    Only use the following tables:

    {table_info}

    
    Here are some synonyms for the keywords of the tables:
    __synonyms_str__
    

    Do not use Select * from

    Question: {input}"""

SQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=SQL_LLM_TEMPLATE
)

def get_sql_lang_prompt(lang='Chinese'):
    # sql_templ = SQL_LANG_TEMPLATE_NO_LIMIT.replace("__lang_str__",lang)
    synonyms = str(config.FIELD_SYNONYM_V2_LITE)[1:-1]
    sql_templ = SQL_LANG_TEMPLATE_NO_LIMIT_SYNONYMS.replace("__lang_str__",lang).replace("__synonyms_str__",synonyms)
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

PRUNE_PROMPT = """Return each element in the Potential Doctor resume fields(in "key":"value" of JSON format) list which is not clearly mentioned in Doctor Resume.
Examples of fields which are not mentioned in Doctor Resume text.
If no non-verified fields are found, return "None".

Doctor Resume:
John P.A. Ioannidis
PROFESSOR OF MEDICINE (STANFORD PREVENTION RESEARCH), OF EPIDEMIOLOGY AND POPULATION HEALTH AND BY COURTESY, OF STATISTICS AND OF BIOMEDICAL DATA SCIENCE
Medicine - Stanford Prevention Research Center
Web page: http://web.stanford.edu/people/jioannid

Potential Doctor Resume Fields:
{
 "name":"John P.A. Ioannidis",
 "positions":"PROFESSOR OF MEDICINE (STANFORD PREVENTION RESEARCH), OF EPIDEMIOLOGY AND POPULATION HEALTH AND BY COURTESY, OF STATISTICS AND OF BIOMEDICAL DATA SCIENCE",
 "department":"Medicine - Stanford Prevention Research Center",
 "web_page":"http://web.stanford.edu/people/jioannid",
 "sex":"male",
 "location":"China"
}

Not Mentioned Fields:
{
 "sex":"male",
 "location":"China"
}

Doctor Resume:
{query_str}

Potential Doctor Resume Fields:
{bulleted_str}

Not Mentioned Fields:
-"""

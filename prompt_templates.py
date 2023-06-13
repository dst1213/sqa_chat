from langchain import PromptTemplate

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

SQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=SQL_LLM_TEMPLATE
)

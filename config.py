import os
from dotenv import load_dotenv

load_dotenv()

LONG_TEXT_EXTRACT_LIMIT = 50000
LONG_TEXT_EXTRACT_MODEL = 'gpt-3.5-turbo-16k'
LONG_TEXT_EXTRACT_REPEAT = 0
LONG_TEXT_EXTRACT_OUTPUT_TYPE = 'txt'  # txt,json

# openai服务配置
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_HOST = os.environ.get("OPENAI_API_BASE")
OPENAI_API_HOST_BAK = os.environ.get("OPENAI_API_BASE_BACKUP")
OPENAI_API_HOST_BAK2 = os.environ.get("OPENAI_API_BASE_BACKUP2")
OPENAI_GPT_MODEL = "gpt-3.5-turbo"
OPENAI_API_HOST_USE = OPENAI_API_HOST_BAK

# 抽取字段的映射
FIELD_SYNONYM_V2 = {"name": ["姓名", "name"],
                 "organization": ["医院机构", "诊所", "药厂", "公司", "hospital", "clinic", "Centers & Institutes"],
                 "department": ["科室", "部门", "department", "Departments / Divisions"],
                 "position": ["职务", "职位", "position", "Academic Appointments", "Administrative Appointments"],
                 "title": ["职称", "title", "Titles"],
                 "phone": ["电话", "contact", "phone", "mobile", "Contact for Research Inquiries"],
                 "email": ["邮箱", "email", "电邮"],
                 "location": ["位置", "地址", "城市", "location", "office location", "Locations",
                              "Locations & Patient Information"],
                 "introduce": ["个人介绍", "自我介绍", "专家介绍", "简介", "about me", "introduce", "biology", "Bio",
                               "Background", "About"],
                 "expertise": ["专长", "擅长", "specialty", "expertise", "interests", "Expertise", "Research Interests",
                               "Specialties", "Areas of Expertise"],
                 "visit_time": ["出诊时间", "出诊信息", "visit time", "visit hours"],
                 "qualification": ["资格证书", "qualification"],
                 "insurance": ["适用医保", "医疗保险", "医保", "insurance", "Accepted Insurance"],
                 "academic": ["学术兼职", "part-time", "academic", "Boards", "Advisory Committees",
                              "Professional Organizations", "Memberships", "Professional Activities"],
                 "work_experience": ["工作经历", "work experience", "career", "short bio"],
                 "education": ["学习经历", "学历", "education", "Professional Education", "Education", "Degrees",
                               "Residencies", "Fellowships", "Board Certifications", "Additional Training",
                               "Education & Professional Summary"],
                 "publications": ["文献著作", "出版", "论文", "publications", "abstract", "all publications",
                                  "selected publications"],
                 "clinical_trial": ["临床研究", "研究", "clinical_trial", "clinical trials",
                                    "Current Research and Scholarly Interests", "Clinical Trials", "Projects",
                                    "Clinical Trial Keywords", "Clinical Trials & Research"],
                 "achievement": ["荣誉成就", "honor", "achievement", "Honors & Awards", "Honors"],
                 "service_language": ["服务语言", "service language", "language"]}
FIELD_SYNONYM_V1 = {"name": ["姓名", "name"],
                 "organization": ["医院机构", "诊所", "药厂", "公司", "hospital", "clinic"],
                 "department": ["科室", "部门", "department"],
                 "position": ["职务", "职位", "position"],
                 "title": ["职称", "title"],
                 "phone": ["电话", "contact", "phone", "mobile"],
                 "email": ["邮箱", "email", "电邮"],
                 "location": ["位置", "地址", "城市", "location", "office location"],
                 "introduce": ["个人介绍", "自我介绍", "专家介绍", "简介", "about me", "introduce","biology"],
                 "expertise": ["专长：", "擅长", "specialty", "expertise", "interests"],
                 "visit_time": ["出诊时间", "出诊信息", "visit time", "visit hours"],
                 "qualification": ["资格证书", "qualification"],
                 "insurance": ["适用医保", "医疗保险", "医保", "insurance"],
                 "academic": ["学术兼职", "part-time", "academic"],
                 "work_experience": ["工作经历", "work experience", "career", "short bio"],
                 "education": ["学习经历", "学历", "education"],
                 "publications": ["文献著作", "出版", "论文", "publications","abstract","all publications","selected publications"],
                 "clinical_trial": ["临床研究", "研究", "clinical_trial", "clinical trials"],
                 "achievement": ["荣誉成就", "honor", "achievement"],
                 "service_language": ["服务语言", "service language", "language"]}



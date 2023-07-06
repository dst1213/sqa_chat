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
                    "expertise": ["专长", "擅长", "specialty", "expertise", "interests", "Expertise",
                                  "Research Interests",
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
                    "service_language": ["服务语言", "service language", "language"],
                    "avatar": ["头像", "head", "profile"],  # ChatGPT不需要此字段！！！
                    }

FIELD_SYNONYM_V1 = {"name": ["姓名", "name"],
                    "organization": ["医院机构", "诊所", "药厂", "公司", "hospital", "clinic"],
                    "department": ["科室", "部门", "department"],
                    "position": ["职务", "职位", "position"],
                    "title": ["职称", "title"],
                    "phone": ["电话", "contact", "phone", "mobile"],
                    "email": ["邮箱", "email", "电邮"],
                    "location": ["位置", "地址", "城市", "location", "office location"],
                    "introduce": ["个人介绍", "自我介绍", "专家介绍", "简介", "about me", "introduce", "biology",'基本資料'],
                    "expertise": ["专长：", "擅长", "specialty", "expertise", "interests"],
                    "visit_time": ["出诊时间", "出诊信息", "visit time", "visit hours"],
                    "qualification": ["资格证书", "qualification"],
                    "insurance": ["适用医保", "医疗保险", "医保", "insurance"],
                    "academic": ["学术兼职", "part-time", "academic"],
                    "work_experience": ["工作经历", "work experience", "career", "short bio",'現職'],
                    "education": ["学习经历", "学历", "education",'學歷'],
                    "publications": ["文献著作", "出版", "论文", "publications", "abstract", "all publications",
                                     "selected publications"],
                    "clinical_trial": ["临床研究", "研究", "clinical_trial", "clinical trials"],
                    "achievement": ["荣誉成就", "honor", "achievement"],
                    "service_language": ["服务语言", "service language", "language"]}

TAG_LANG_MAPPING = {
    "publications": {'tag_type': 'li', 'zh-cn': ['发表'], 'en': ['publications']},
    "clinical trials": {'tag_type': 'li', 'en': ["clinical trials"]},
    "achievement": {'tag_type': 'li', 'en': ["achievement"], 'ru': ['достижения']},
    "expertise": {'tag_type': 'li', 'en': ["expertise"], 'ru': ['профессиональных']},
    "academic": {'tag_type': 'li', 'en': ["academic"], 'ru': ['академиях', 'Членство', 'деятельность']},
    "work_experience": {'tag_type': 'li', 'en': ["work experience", "career", "short bio"],
                        'ru': ['справка']},
    "education": {'tag_type': 'li', 'en': ["education"], 'ru': ['бразование']},
}

MARKDOWN_KEYWORDS = ['Academic Appointments', 'clinical trials', 'Administrative Appointments', 'Areas of Expertise',
                     'Professional Organizations', 'Professional Activities', 'About', 'Projects', 'bio',
                     'Contact for Research Inquiries', 'Clinical Trials & Research', 'Board Certifications',
                     'Clinical Trial Keywords', 'Education & Professional Summary', 'Locations & Patient Information',
                     'Honors', 'Titles', 'Contact', 'Clinical Trials', 'Current Research and Scholarly Interests',
                     'Departments / Divisions', 'Centers & Institutes', 'All Publications', 'Specialties',
                     'Additional Training', 'Education', 'Residencies', 'Selected Publications', 'Advisory Committees',
                     'Abstract', 'Accepted Insurance', 'publications', 'Expertise', 'Professional Education', 'biology',
                     'abstract', 'Research Interests', 'BioBackground', 'Degrees', 'Boards', 'Locations',
                     'Honors & Awards',
                     'Fellowships', 'Memberships','學歷','基本資料','現職']

SERVICE_LANGUAGES = {'ru': 'Russian', 'en': 'English', 'zh': 'Chinese', 'fr': 'French', 'nl': 'Dutch', 'kr': 'Korean',
                     'es': 'Spanish','he':'Hebrew','ar':'Arabic','zh-cn':'Simplified Chinese','zh-tw':'Traditional Chinese'}

FIELD_NEED_CHECK = ['name','phone','education','organization','department','position','title','email','location']

PHONE_LANG_MAPPING = {'en': r'\(?(\d{3})\)?[ -.]?(\d{3})[ -.]?(\d{4})'}

REMOVE_INFO = ['版權','copyright','瀏覽統計']

SITE_PATTERN_MAPPING = {'sysucc':{'publications':r'\d+\.[\s\S]*?(?=\d+\.|$)|\[\d+\][\s\S]*?(?=\[\d+\]|$)|\d+．[\s\S]*?(?=\d+．|$)'}}

MUST_SYMBOLS = {'email':'@'}
import json
from pprint import pprint


def crawl_to_db():
    with open("test/data/url_example_py.json") as f:
        _data = f.read()
    data = json.loads(_data)
    doctors = [{"did": "tom_123", "name": data['name'], "english_name": data["name"], "email": data["email"],
                "sex": "female", "title": data["title"],
                "position": "{}".format({"institution": data["organization"], "department": data["department"],
                                         "position": data["position"]}),
                "contact": "{}".format(
                    {"location": data["location"], "phone": data["phone"], "email": data["email"],
                     "fax": data["phone"]}),
                "biography": data["introduce"],
                "expertise": data["expertise"],
                "visit_time": "{}".format(
                    {"visit_info": "not provided", "visit_location": data["location"],
                     "visit_time": data["visit_time"]}),
                "qualification": "{}".format(
                    {"certification": data["qualification"], "fellowship": "not provided", "npi": "not provided"}),
                "insurance": data["insurance"],
                "language": data["language"]
                }]
    experiences = [{
        "type": "career",
        "info": data["work_experience"],
        "time": ""
    },
        {
            "type": "education",
            "info": data["education"],
            "time": ""
        }
    ]
    achievements = [{
        "type": "achievement",
        "info": data["achievement"],
        "time": ""
    }]
    publications = [{"type": "publications", "info": item, "time": ""} for item in data["publications"]]
    researches = [{"type": "clinical_trials",
                   "info": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction",
                   "time": ""}]
    pubmed = [{"pid": id, "title": "not provided"} for id in data["pmid"]]
    clinical_trials = [{"nct_no": "NCT00080002",
                        "brief_title": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction"}]

    res = {"doctor": doctors, "personal_experience": experiences, "achievements": achievements,
           "publications": publications, "medical_research": researches, "pubmed_detail": pubmed,
           "clinical_trials_detail": clinical_trials}

    return res


def crawl_to_db2():
    with open("test/data/url_example_py.json") as f:
        _data = f.read()
    data = json.loads(_data)
    doctors = [{"doctor_id": "tom_123", "name": data['name'], "english_name": data["name"], "email": data["email"],
                "sex": "female", "title": data["title"],
                "position": "{}".format({"institution": data["organization"], "department": data["department"],
                                         "position": data["position"]}),
                "contact": "{}".format(
                    {"location": data["location"], "phone": data["phone"], "email": data["email"],
                     "fax": data["phone"]}),
                "biography": data["introduce"],
                "expertise": data["expertise"],
                "visit_time": "{}".format(
                    {"visit_info": "not provided", "visit_location": data["location"],
                     "visit_time": data["visit_time"]}),
                "qualification": "{}".format(
                    {"certification": data["qualification"], "fellowship": "not provided", "npi": "not provided"}),
                "insurance": data["insurance"],
                "language": data["language"]
                }]
    experiences = [{
        "doctor_id": "tom_123",
        "type": "career",
        "info": data["work_experience"],
        "time": ""
    },
        {
            "doctor_id": "tom_123",
            "type": "education",
            "info": data["education"],
            "time": ""
        }
    ]
    achievements = [{
        "doctor_id": "tom_123",
        "type": "achievement",
        "info": data["achievement"],
        "time": ""
    }]
    publications = [{"doctor_id": "tom_123", "type": "publications", "info": item, "time": ""} for item in
                    data["publications"]]
    researches = [{"doctor_id": "tom_123", "type": "clinical_trials",
                   "info": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction",
                   "time": ""}]
    pubmed = [{"doctor_id": "tom_123", "pid": id, "title": "not provided"} for id in data["pmid"]]
    clinical_trials = [{"doctor_id": "tom_123", "nct_no": "NCT00080002",
                        "brief_title": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction",
                        "inclusion_criteria": """
                                            - Woman older than 18 years
                                            Low-risk gestational trophoblastic neoplasia according to FIGO score (FIGO score ≤ 6) with indication of methotrexate as first line treatment
                                            Patients with Eastern Cooperative Oncology Group (ECOG) performance status ≤ 2
                                            Patients with adequate bone marrow function measured within 28 days prior to administration of study treatment as defined below

                                            Absolute granulocyte count ≥ 1.5 x 10 9 /L
                                            Platelet count ≥ 100 x 10 9 /L
                                            Haemoglobin ≥ 9.0 g/dL (may have been blood transfused)
                                            Patients with adequate renal function:

                                            * Calculated creatinine clearance ≥ 30 ml/min according to the Cockcroft-Gault formula (or local institutional standard method)

                                            Patients with adequate hepatic function

                                            *Serum bilirubin ≤ 1.5 x UNL and AST/ALT ≤ 2.5 X UNL (≤ 5 X UNL for patients with liver metastases)

                                            Patients must have a life expectancy ≥ 16 weeks
                                            Confirmation of non-childbearing status for women of childbearing potential.
                                            An evolutive pregnancy can be ruled out in the following cases:

                                            in case of a previous hysterectomy
                                            if serum hCG level ≥ 2 000 IU/L and no intra or extra-uterine gestational sac is detected on pelvic ultrasound
                                            if serum hCG level < 2 000 IU/L on a first measurement and serum hCG increases <100% on a second measurement performed 3 days later.

                                            Highly effective contraception if the risk of conception exists. (Note: The effects of the trial drug on the developing human fetus are unknown; thus, women of childbearing potential must agree to use 2 highly effective contraceptions, defined as methods with a failure rate of less than 1 % per year. Highly effective contraception is required at least 28 days prior, throughout and for at least 12 months after avelumab treatment.
                                            Patients who gave its written informed consent to participate to the study
                                            Patients affiliated to a social insurance regime
                                            Patient is willing and able to comply with the protocol for the duration of the treatment
                        """,
                        "exclusion_criteria": """
                                            Prior therapy with an anti-PD-1, anti-PD-L1, anti-PD-L2, anti-CD137, or anti- CTLA 4 antibody (including ipilimumab, tremelimumab or any other antibody or drug specifically targeting T-cell costimulation or immune checkpoint pathways).
                                            Illness, incompatible with avelumab, such as congestive heart failure; respiratory distress; liver failure; uncontrolled epilepsy; allergy.
                                            Patients with a known allergic hypersensitivity to methotrexate or any of the other ingredients (sodium chloride, sodium hydroxide, and hydrochloric acid if excipient)
                                            Patients with second primary cancer, except: adequately treated non-melanoma skin cancer, curatively treated in-situ cancer of the cervix, or other solid tumours curatively treated with no evidence of disease for ≥ 5 years.
                                            All subjects with brain metastases, except those meeting the following criteria:

                                            Brain metastases that have been treated locally and are clinically stable for at least 2 weeks prior to enrolment, No ongoing neurological symptoms that are related to the brain localization of the disease (sequelae that are a consequence of the treatment of the brain metastases are acceptable).
                                            Subjects with brain metastases must be either off steroids except a stable or decreasing dose of <10mg daily prednisone (or equivalent).
                                            Patients receiving any systemic chemotherapy, radiotherapy (except for palliative reasons), within 2 weeks from the last dose prior to study treatment (or a longer period depending on the defined characteristics of the agents used). The patient can receive a stable dose of bisphosphonates for bone metastases, before and during the study as long as these were started at least 4 weeks prior to treatment with study drug.
                                            Persistent toxicities (>=CTCAE grade 2) with the exception of alopecia and sensory neuropathy, caused by previous cancer therapy.
                                            Treatment with other investigational agents.
                                            Bowel occlusive syndrome, inflammatory bowel disease, immune colitis, or other gastro-intestinal disorder that does not allow oral medication such as malabsorption.
                                            Stomatitis, ulcers of the oral cavity and known active gastrointestinal ulcer disease
                                            Clinically significant (i.e., active) and severe cardiovascular disease according to investigator opinion such as myocardial infarction (< 6 months prior to enrollment)
                                            Patients with immune pneumonitis, pulmonary fibrosis
                                            Known severe hypersensitivity reactions to monoclonal antibodies, any history of anaphylaxis, or uncontrolled asthma (ie, 3 or more features of partially controlled asthma Global Initiative for Asthma 2011).
                                            Known human immunodeficiency virus (HIV) or acquired immunodeficiency syndrome (AIDS) related illness.
                                            Active infection requiring systemic therapy.
                                            Positive test for HBV surface antigen and / or confirmatory HCV RNA (if anti-HCV antibody tested positive)
                                            Administration of a live vaccine within 30 days prior to study entry.
                                            Current or prior use of immunosuppressive medication within 7 days prior to start of study treatment.
                                            The following are exceptions to this exclusion criterion:

                                            Intranasal, inhaled, topical steroids, or local steroid injections (eg, intra-articular injection);
                                            Systemic corticosteroids at physiologic doses not to exceed 10 mg/day of prednisone or equivalent;
                                            Steroids as premedication for hypersensitivity reactions (eg, CT scan premedication).

                                            Active autoimmune disease that might deteriorate when receiving an immunostimulatory agents.
                        """}]

    res = {"doctor": doctors, "personal_experience": experiences, "achievements": achievements,
           "publications": publications, "medical_research": researches, "pubmed_detail": pubmed,
           "clinical_trials_detail": clinical_trials}

    return res


def crawl_to_db3():
    with open("test/data/url_example_py.json") as f:
        _data = f.read()
    # with open("test/data/ct.txt") as ff:
    #     _ct_data = f.read()
    data = json.loads(_data)
    doctors = [{"doctor_id": "tom_123", "name": data['name'], "english_name": data["name"], "email": data["email"],
                "sex": "female",
                "title_position": "{}".format({"institution": data["organization"], "department": data["department"],
                                               "position": data["position"], "title": data["title"]}),
                "biography": data["introduce"],
                "expertise": data["expertise"],
                "visit_time": "{}".format(
                    {"visit_info": "not provided", "visit_location": data["location"],
                     "visit_time": data["visit_time"]}),
                "qualification": "{}".format(
                    {"certification": data["qualification"], "fellowship": "not provided", "npi": "not provided"}),
                "insurance": data["insurance"],
                "language": data["language"]
                }]
    contacts = [{"doctor_id": "tom_123", "location": data["location"], "phone": data["phone"], "email": data["email"],
                 "fax": data["phone"]}]
    experiences = [{
        "doctor_id": "tom_123",
        "type": "career",
        "info": data["work_experience"],
        "time": ""
    },
        {
            "doctor_id": "tom_123",
            "type": "education",
            "info": data["education"],
            "time": ""
        }
    ]
    achievements = [{
        "doctor_id": "tom_123",
        "type": "achievement",
        "info": data["achievement"],
        "time": ""
    }]
    publications = [{"doctor_id": "tom_123", "type": "publications", "info": item, "time": ""} for item in
                    data["publications"]]
    researches = [{"doctor_id": "tom_123", "type": "clinical_trials",
                   "info": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction",
                   "time": ""}]
    pubmed = [{"doctor_id": "tom_123", "pid": id, "title": "not provided"} for id in data["pmid"]]
    clinical_trials = [{
        "doctor_id": "tom_123",
        "identification_module_nct_id": "NCT00080002",
        "identification_module_org_study_id_info_id": "CAM-9011",
        "identification_module_organization_full_name": "Enzon Pharmaceuticals, Inc.",
        "identification_module_organization_class": "INDUSTRY",
        "identification_module_brief_title": "Efficacy of Pegamotecan (PEG-Camptothecin) in Localized or Metastatic Cancer of the Stomach or Gastroesophageal Junction",
        "identification_module_official_title": "Effectiveness and Safety Study of Pegamotecan (PEG-Camptothecin) in Patients With Locally Advanced or Metastatic Cancer of the Stomach or Gastroesophageal Junction Who Have Relapsed or Progressed Following a Previous Chemotherapy Treatment",
        "status_module_status_verified_date": "2005-03",
        "status_module_overall_status": "TERMINATED",
        "status_module_start_date_struct_date": "2003-12",
        "status_module_study_first_submit_date": "2004-03-19",
        "status_module_study_first_submit_qc_date": "2004-03-22",
        "status_module_study_first_post_date_struct_date": "2004-03-23",
        "status_module_study_first_post_date_struct_type": "ESTIMATED",
        "status_module_last_update_submit_date": "2012-09-05",
        "status_module_last_update_post_date_struct_date": "2012-09-06",
        "status_module_last_update_post_date_struct_type": "ESTIMATED",
        "sponsor_collaborators_module_lead_sponsor_name": "Enzon Pharmaceuticals, Inc.",
        "sponsor_collaborators_module_lead_sponsor_class": "INDUSTRY",
        "description_module_brief_summary": "The purpose of this study is to evaluate the safety and efficacy of pegamotecan (PEG-camptothecin) in patients with pathologically-diagnosed locally advanced or metastatic adenocarcinoma of the stomach or gastroesophageal junction who have relapsed or progressed following one prior chemotherapy treatment regimen.",
        "conditions_module_conditions": [
            "Cancer of Stomach",
            "Gastroesophageal Cancer"
        ],
        "conditions_module_keywords": [
            "cancer",
            "gastric",
            "gastroesophageal junction",
            "neoplasms",
            "gastric cancer",
            "gastric neoplasms"
        ],
        "design_module_study_type": "INTERVENTIONAL",
        "design_module_phases": ["PHASE2"],
        "design_module_design_info_allocation": "NON_RANDOMIZED",
        "design_module_design_info_intervention_model": "SINGLE_GROUP",
        "design_module_design_info_primary_purpose": "TREATMENT",
        "design_module_design_info_masking_info_masking": "NONE",
        "arms_interventions_module_interventions": [{
            "type": "DRUG",
            "name": "Pegamotecan"
        }],
        "eligibility_module_eligibility_criteria": "Inclusion Criteria:\n\n* Pathologically confirmed diagnosis of adenocarcinoma of the stomach or gastroesophageal junction.\n* Disease measurable in at least one dimension.\n* Target tumors outside of prior radiation field(s).\n* An Eastern Cooperative Oncology Group (ECOG) performance scale score of 0 or 1\n* Adequate hematologic profile, as determined by hemoglobin, platelet, and neutrophil count.\n* Adequate renal function, as determined by serum creatinine and serum albumin measurements.\n* Adequate liver function, as determined by total bilirubin and transaminases levels. Transaminases may be \\<= 5.0x ULN if due to metastatic disease in the liver.\n* Fully recovered from prior surgery.\n* No history of hemorrhagic cystitis.\n* No microscopic hematuria (\\>10 RBC/hpf) unless documented to be due to an infection or non-bladder origin.\n* Capable of understanding the protocol requirements and risks and providing written informed consent.\n\nExclusion Criteria:\n\n* Concurrent serious medical illness unrelated to tumor within the past 6 months.\n* Known chronic infectious disease, such as AIDS or hepatitis (screening for hepatitis and HIV will not be performed).\n* Positive screening pregnancy test or is breast-feeding.\n* Female or male subject of reproductive capacity who is unwilling to use methods appropriate to prevent pregnancy during the course of this study.\n* Receiving concurrent chemotherapy, investigational agents, radiotherapy, surgery, or has received wide field radiation within the previous 4 weeks.\n* History of another malignancy (except basal and squamous cell carcinomas of the skin and carcinoma in situ of the cervix) within the last 5 years.\n* Known or clinically suspected brain metastases.\n* Received more than one prior regimen of chemotherapy for locally advanced or metastatic adenocarcinoma of the stomach or GE junction.\n* Received prior neoadjuvant and/or adjuvant cytotoxic chemotherapy\n* Received any investigational drug within the last 30 days.\n* Not fully recovered from any prior, and from any reversible side effects related to the administration of cytotoxic chemotherapy, investigational agents, or radiation therapy.\n* Prior treatment with a camptothecin analog.",
        "eligibility_module_healthy_volunteers": False,
        "eligibility_module_sex": "ALL",
        "eligibility_module_minimum_age": "18 Years",
        "eligibility_module_std_ages": [
            "ADULT",
            "OLDER_ADULT"
        ]
    },
        {
            "doctor_id": "tom_123",
            "identification_module_nct_id": "NCT00080003",
            "identification_module_org_study_id_info_id": "CAM-9011",
            "identification_module_organization_full_name": "Enzon Pharmaceuticals, Inc.",
            "identification_module_organization_class": "INDUSTRY",
            "identification_module_brief_title": "A Dose-Finding Study of AG-348 in Sickle Cell Disease",
            "identification_module_official_title": "A Pilot Study to Evaluate the Safety, Tolerability, Pharmacokinetics, and Pharmacodynamics of Escalating Multiple Oral Doses of AG-348 in Subjects With Stable Sickle Cell Disease",
            "status_module_status_verified_date": "2005-03",
            "status_module_overall_status": "TERMINATED",
            "status_module_start_date_struct_date": "2003-12",
            "status_module_study_first_submit_date": "2004-03-19",
            "status_module_study_first_submit_qc_date": "2004-03-22",
            "status_module_study_first_post_date_struct_date": "2004-03-23",
            "status_module_study_first_post_date_struct_type": "ESTIMATED",
            "status_module_last_update_submit_date": "2012-09-05",
            "status_module_last_update_post_date_struct_date": "2012-09-06",
            "status_module_last_update_post_date_struct_type": "ESTIMATED",
            "sponsor_collaborators_module_lead_sponsor_name": "Enzon Pharmaceuticals, Inc.",
            "sponsor_collaborators_module_lead_sponsor_class": "INDUSTRY",
            "description_module_brief_summary": "The purpose of this study is to evaluate the safety and efficacy of pegamotecan (PEG-camptothecin) in patients with pathologically-diagnosed locally advanced or metastatic adenocarcinoma of the stomach or gastroesophageal junction who have relapsed or progressed following one prior chemotherapy treatment regimen.",
            "conditions_module_conditions": [
                "Cancer of Stomach",
                "Gastroesophageal Cancer"
            ],
            "conditions_module_keywords": [
                "cancer",
                "gastric",
                "gastroesophageal junction",
                "neoplasms",
                "gastric cancer",
                "gastric neoplasms"
            ],
            "design_module_study_type": "INTERVENTIONAL",
            "design_module_phases": ["PHASE2"],
            "design_module_design_info_allocation": "NON_RANDOMIZED",
            "design_module_design_info_intervention_model": "SINGLE_GROUP",
            "design_module_design_info_primary_purpose": "TREATMENT",
            "design_module_design_info_masking_info_masking": "NONE",
            "arms_interventions_module_interventions": [{
                "type": "DRUG",
                "name": "Pegamotecan"
            }],
            "eligibility_module_eligibility_criteria": "Inclusion Criteria:\n\n* Pathologically confirmed diagnosis of adenocarcinoma of the stomach or gastroesophageal junction.\n* Disease measurable in at least one dimension.\n* Target tumors outside of prior radiation field(s).\n* An Eastern Cooperative Oncology Group (ECOG) performance scale score of 0 or 1\n* Adequate hematologic profile, as determined by hemoglobin, platelet, and neutrophil count.\n* Adequate renal function, as determined by serum creatinine and serum albumin measurements.\n* Adequate liver function, as determined by total bilirubin and transaminases levels. Transaminases may be \\<= 5.0x ULN if due to metastatic disease in the liver.\n* Fully recovered from prior surgery.\n* No history of hemorrhagic cystitis.\n* No microscopic hematuria (\\>10 RBC/hpf) unless documented to be due to an infection or non-bladder origin.\n* Capable of understanding the protocol requirements and risks and providing written informed consent.\n\nExclusion Criteria:\n\n* Concurrent serious medical illness unrelated to tumor within the past 6 months.\n* Known chronic infectious disease, such as AIDS or hepatitis (screening for hepatitis and HIV will not be performed).\n* Positive screening pregnancy test or is breast-feeding.\n* Female or male subject of reproductive capacity who is unwilling to use methods appropriate to prevent pregnancy during the course of this study.\n* Receiving concurrent chemotherapy, investigational agents, radiotherapy, surgery, or has received wide field radiation within the previous 4 weeks.\n* History of another malignancy (except basal and squamous cell carcinomas of the skin and carcinoma in situ of the cervix) within the last 5 years.\n* Known or clinically suspected brain metastases.\n* Received more than one prior regimen of chemotherapy for locally advanced or metastatic adenocarcinoma of the stomach or GE junction.\n* Received prior neoadjuvant and/or adjuvant cytotoxic chemotherapy\n* Received any investigational drug within the last 30 days.\n* Not fully recovered from any prior, and from any reversible side effects related to the administration of cytotoxic chemotherapy, investigational agents, or radiation therapy.\n* Prior treatment with a camptothecin analog.",
            "eligibility_module_healthy_volunteers": False,
            "eligibility_module_sex": "ALL",
            "eligibility_module_minimum_age": "18 Years",
            "eligibility_module_std_ages": [
                "ADULT",
                "OLDER_ADULT"
            ]
        }
    ]

    new_ct = []
    for item in clinical_trials:
        for k, v in item.items():
            if isinstance(v, list):
                item[k] = str(item[k])
        new_ct.append(item)

    res = {"doctor": doctors, "personal_experience": experiences, "achievements": achievements,
           "publications": publications, "medical_research": researches, "pubmed_detail": pubmed,
           "clinical_trials_detail": new_ct, "contacts": contacts}

    return res


if __name__ == "__main__":
    res = crawl_to_db()
    pprint(res)
import re

def extract_pubmed_ids(text):
    # pattern = r"(?:PubMed (?:PMID|Central PMCID): |PMID: |^)(\d+)"
    pattern = r"(?:PubMed (?:PMID|Central PMCID): |PMID: |^|PMID:)(\d+)"

    pmids = re.findall(pattern, text)
    return pmids

# 示例一
text1 = """
HT, Powe NR, Nelson C, Ford DE. Race, gender, and partnership in the patient-physician relationship. JAMA. 1999 Aug 11;282(6):583-9. PubMed PMID: 10450723

Cooper LA, Roter DL, Johnson RL, Ford DE, Steinwachs DM, Powe NR. Patient-centered communication, ratings of care, and concordance of patient and physician race. Ann Intern Med. 2003 Dec 2;139(11):907-15. PubMed PMID: 14644893

Johnson RL, Roter D, Powe NR, Cooper LA. Patient race/ethnicity and quality of patient-physician communication during medical visits. Am J Public Health. 2004 Dec;94(12):2084-90. PubMed PMID: 15569958; PubMed Central PMCID: PMC1448596.
"""

pmids1 = extract_pubmed_ids(text1)
print(pmids1)

# 示例二
text2 = """
For a comprehensive list of Dr. Gandara's publications, please click here (opens new window).

Ranganath H, Jain AL, Smith JR, Ryder J, Chaudry A, Miller E, Hare F, Valasareddy P, Seitz RS, Hout DR, Varga MG, Schweitzer BL, Nielsen TJ, Mullins J, Ross DT, Gandara DR, Vidal GA. Association of a novel 27-gene immuno-oncology assay with efficacy of immune checkpoint inhibitors in advanced non-small cell lung cancer. BMC Cancer. 2022 Apr 14;22(1):407. doi:10.1186/s12885-022-09470-y. PMID:35421940.

Sun H, Cao S, Mashl RJ, Mo CK, Zaccaria S, Wendl MC, Davies SR, Bailey MH, Primeau TM, Hoog J, Mudd JL, Dean DA 2nd, Patidar R, Chen L, Wyczalkowski MA, Jayasinghe RG, Rodrigues FM, Terekhanova NV, Li Y, Lim KH, Wang-Gillam A, Van Tine BA, Ma CX, Aft R, Fuh KC, Schwarz JK, Zevallos JP, Puram SV, Dipersio JF; NCI PDXNet Consortium, Davis-Dusenbery B, Ellis MJ, Lewis MT, Davies MA, Herlyn M, Fang B, Roth JA, Welm AL, Welm BE, Meric-Bernstam F, Chen F, Fields RC, Li S, Govindan R, Doroshow JH, Moscow JA, Evrard YA, Chuang JH, Raphael BJ, Ding L. Author Correction: Comprehensive characterization of 536 patient-derived xenograft models prioritizes candidates for targeted treatment. Nat Commun. 2022 Jan 7;13(1):294. doi:10.1038/s41467-021-27678-7. Erratum for: Nat Commun. 2021 Aug 24;12(1):5086. PMID:34996889.

Gadgeel S, Hirsch FR, Kerr K, Barlesi F, Park K, Rittmeyer A, Zou W, Bhatia N, Koeppen H, Paul SM, Shames D, Yi J, Matheny C, Ballinger M, McCleland M, Gandara DR.
"""

pmids2 = extract_pubmed_ids(text2)
print(pmids2)

# 示例三
text3 = """
Three-Year Safety, Tolerability, and Health-Related Quality of Life Outcomes of Adjuvant Osimertinib in Patients with Resected Stage IB–IIIA EGFR-Mutated Non-Small Cell Lung Cancer: Updated Analysis from the Phase 3 ADAURA Trial
John T, Grohé C, Goldman J, Shepherd F, de Marinis F, Kato T, Wang Q, Su W, Choi J, Sriuranpong V, Melotti B, Fidler M, Chen J, Albayaty M, Stachowiak M, Taggart S, Wu Y, Tsuboi M, Herbst R, Majem M. Three-Year Safety, Tolerability, and Health-Related Quality of Life Outcomes of Adjuvant Osimertinib in Patients with Resected Stage IB–IIIA EGFR-Mutated Non-Small Cell Lung Cancer: Updated Analysis from the Phase 3 ADAURA Trial Journal Of Thoracic Oncology 2023 PMID: 37236398, DOI: 10.1016/j.jtho.2023.05.015.

Randomized Phase II Trial Comparing Bevacizumab Plus Carboplatin and Paclitaxel With Carboplatin and Paclitaxel Alone in Previously Untreated Locally Advanced or Metastatic Non-Small-Cell Lung Cancer
Johnson D, Fehrenbacher L, Novotny W, Herbst R, Nemunaitis J, Jablons D, Langer C, DeVore R, Gaudreault J, Damico L, Holmgren E, Kabbinavar F. Randomized Phase II Trial Comparing Bevacizumab Plus Carboplatin and Paclitaxel With Carboplatin and Paclitaxel Alone in Previously Untreated Locally Advanced or Metastatic Non-Small-Cell Lung Cancer Journal Of Clinical Oncology 2023, 41: 2305-2312. PMID: 37126944, DOI: 10.1200/jco.22.02543.
"""

pmids3 = extract_pubmed_ids(text3)
print(pmids3)

# 示例四
text4 = """
Dacomitinib versus erlotinib in patients with EGFR-mutated advanced nonsmall-cell lung cancer (NSCLC): pooled subset analyses from two randomized trials. Ramalingam SS, O'Byrne K, Boyer M, Mok T, Jänne PA, Zhang H, Liang J, Taylor I, Sbar EI, Paz-Ares L. Ann Oncol. 2016 Jul;27(7):1363. doi: 10.1093/annonc/mdw221. Epub 2016 May 30. No abstract available. PMID: 27240994
Quintanal-Villalonga A, Ojeda-Márquez L, Marrugal A, Yagüe P, Ponce-Aix S, Salinas A, Carnero A, Ferrer I, Molina-Pinelo S, Paz-Ares L*. The FGFR4-388arg Variant Promotes Lung Cancer Progression by N-Cadherin Induction. Sci Rep. 2018; 8: 2394. doi: 10.1038/s41598-018-20570-3.
Paz-Ares L*, Tan EH, O'Byrne K, Zhang L, Hirsh V, Boyer M, Yang JC, Mok T, Lee KH, Lu S, Shi Y, Lee DH, Laskin J, Kim DW, Laurie SA, Kölbeck K, Fan J, Dodd N, Märten A, Park K. Afatinib versus gefitinib in patients with EGFR mutation-positive advanced non-small-cell lung cancer: overall survival data from the phase IIb LUX-Lung 7 trial. Ann Oncol. 2017; 28:270-277. doi: 10.1093/annonc/mdw611.
*Corresponding author
"""
pmids4 = extract_pubmed_ids(text4)
print(pmids4)
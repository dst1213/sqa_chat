import re


def extract_publications(content):
    publications = []
    pattern = r'\[(.*?)\]'  # 正则表达式提取publication内容

    for line in content.splitlines():
        match = re.search(pattern, line)
        if match:
            publications.append(line)  # 添加publication到列表

    return publications


content = '''
### Selected Publications

  * Malison RT, McCance E, Carpenter LL, Baldwin RM, Seibyl JP, Price LH, Kosten TR, Innis RB"[[123I]beta-CIT SPECT imaging of dopamine transporter availability after mazindol administration in human cocaine addicts.](https://ncbi.nlm.nih.gov/pubmed/?term=9676890)." _Psychopharmacology (Berl.)._ 1998 Jun;137(4):321-5. Pubmed PMID: [9676890](https://ncbi.nlm.nih.gov/pubmed/?term=9676890)
  * Kosten TR, Rounsaville BJ, Kleber HD"[A 2.5-year follow-up of cocaine use among treated opioid addicts. Have our treatments helped?](https://ncbi.nlm.nih.gov/pubmed/?term=3827521)." _Arch. Gen. Psychiatry._ 1987 Mar;44(3):281-4. Pubmed PMID: [3827521](https://ncbi.nlm.nih.gov/pubmed/?term=3827521)
  * Kosten TR, Rounsaville BJ, Kleber HD"[A 2.5 year follow-up of treatment retention and reentry among opioid addicts.](https://ncbi.nlm.nih.gov/pubmed/?term=3806731)." _J Subst Abuse Treat._ 1986;3(3):181-9. Pubmed PMID: [3806731](https://ncbi.nlm.nih.gov/pubmed/?term=3806731)
  * Kosten TR, Rounsaville BJ, Kleber HD"[A 2.5-year follow-up of depression, life crises, and treatment effects on abstinence among opioid addicts.](https://ncbi.nlm.nih.gov/pubmed/?term=3729667)." _Arch Gen Psychiatry._ 1986 Aug;733-8. Pubmed PMID: [3729667](https://ncbi.nlm.nih.gov/pubmed/?term=3729667)
'''

publications = extract_publications(content)
print(publications)

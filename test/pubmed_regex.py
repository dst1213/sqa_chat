import re
import json

def remove_links(text):
    pattern = r'<a\b[^>]*>(.*?)</a>'
    return re.sub(pattern, r'\1', text)

def get_pubmed_data(html):
    pubmed_data = []

    pattern = r'<li><div>.*?<span>.*?</span><span>(.*?)</span>.*?PMID: <a href=(.*?)>(\d+)</a>.*?</div>'
    matches = re.findall(pattern, html, re.DOTALL)

    for match in matches:
        title = match[0].strip()
        url = 'https:' + match[1].strip()
        pmid = match[2].strip()

        title = remove_links(title)
        data = {
            'title': title,
            'PMID': pmid,
            'URL': url
        }

        pubmed_data.append(data)

    return pubmed_data


# Example HTML
html = '''
<div><div><div><img src=https://profiles.uchicago.edu/profiles/Profile/Modules/PropertyList/images/minusSign.gif alt=Collapse> selected publications</div><div><div><div><div> Publications listed below are automatically derived from MEDLINE/PubMed and other sources, which might result in incorrect or missing publications. Faculty can <a href="https://profiles.uchicago.edu/profiles/login/default.aspx?pin=send&method=login&edit=true">login</a> to make corrections and additions. </div><div><a>Newest</a>   |   <a>Oldest</a>   |   <a>Most Cited</a>   |   <a>Most Discussed</a>   |   <a>Timeline</a>   |   <a>Field Summary</a>   |   <a>Plain Text</a></div><div><span>PMC Citations</span> indicate the number of times the publication was cited by articles in PubMed Central, and the <span>Altmetric</span> score represents citations in news articles and social media. (Note that publications are often cited in additional ways that are not shown here.) <span>Fields</span> are based on how the National Library of Medicine (NLM) classifies the publication's journal and might not represent the specific topic of the publication. <span>Translation</span> tags are based on the publication type and the MeSH terms NLM assigns to the publication. Some publications (especially newer ones and publications not in PubMed) might not yet be assigned Field or Translation tags.) Click a Field or Translation tag to filter the publications. </div><div><div><ol><li><div><span></span><span>Shah HA, Fischer JH, Venepalli NK, Danciu OC, Christian S, Russell MJ, Liu LC, <b>Zacny JP</b>, Dudek AZ. Phase I Study of Aurora A Kinase Inhibitor Alisertib (MLN8237) in Combination With Selective VEGFR Inhibitor Pazopanib for Therapy of Advanced Solid Tumors. Am J Clin Oncol. 2019 05; 42(5):413-420.</span><span> PMID: <a href=//www.ncbi.nlm.nih.gov/pubmed/30973373>30973373</a>.</span></div><div> Citations: <a href=https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/30973373/citedby/ ><span>5</span></a><span>  <span></span></span>   Fields: <div><a>Neo<span> Neoplasms</span></a></div>   Translation:<a>Humans</a><a>CT<span>Clinical Trials</span></a></div></li><li><div><span></span><span><a href=https://profiles.uchicago.edu/profiles/profile/2101363>Fong R</a>, Wang L, <b>Zacny JP</b>, Khokhar S, <a href=https://profiles.uchicago.edu/profiles/profile/39012>Apfelbaum JL</a>, Fox AP, <a href=https://profiles.uchicago.edu/profiles/profile/38884>Xie Z</a>. Caffeine Accelerates Emergence from Isoflurane Anesthesia in Humans: A Randomized, Double-blind, Crossover Study. Anesthesiology. 2018 11; 129(5):912-920.</span><span> PMID: <a href=//www.ncbi.nlm.nih.gov/pubmed/30044241>30044241</a>; PMCID: <a href=//www.ncbi.nlm.nih.gov/pmc/articles/PMC6191316>PMC6191316</a>.</span></div><div> Citations: <a href=https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/30044241/citedby/ ><span>18</span></a><span>  <span></span></span>   Fields: <div><a>Ane<span> Anesthesiology</span></a></div>   Translation:<a>Humans</a></div></li></ol></div></div></div></div>
'''

pubmed_data = get_pubmed_data(html)

# Convert to JSON
result = {"pubmed": pubmed_data}
json_result = json.dumps(result, indent=4)
print(json_result)

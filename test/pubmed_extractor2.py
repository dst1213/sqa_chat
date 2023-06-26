import re
import json

import requests


def get_pubmed_data(html):
    pubmed_data = []

    pattern = r'<li>.*?<span>(.*?)</span>.*?<a href=".*?">.*?</a>.*?<em>.*?</em>.*?Pubmed PMID: <a href="(.*?)">(.*?)</a>.*?</li>'
    matches = re.findall(pattern, html, re.DOTALL)

    for match in matches:
        title = match[0].strip()
        url = match[1].strip()
        pmid = match[2].strip()

        data = {
            'title': title,
            'PMID': pmid,
            'URL': url
        }

        pubmed_data.append(data)

    return pubmed_data


# Example HTML
html = '''
<div class="col-md-6">
                                  <h3 class="user--details">Selected Publications</h3>
            <ul>
                                                                <li>
                    <span>Malison RT, McCance E, Carpenter LL, Baldwin RM, Seibyl JP, Price LH, Kosten TR, Innis RB</span>                    <span>"<a href="https://ncbi.nlm.nih.gov/pubmed/?term=9676890">[123I]beta-CIT SPECT imaging of dopamine transporter availability after mazindol administration in human cocaine addicts.</a>."</span>                    <span><em>Psychopharmacology (Berl.).</em> 1998 Jun;137(4):321-5.</span>
                    Pubmed PMID: <a href="https://ncbi.nlm.nih.gov/pubmed/?term=9676890">9676890</a>                  </li>
                                                                                                <li>
                    <span>Kosten TR, Rounsaville BJ, Kleber HD</span>                    <span>"<a href="https://ncbi.nlm.nih.gov/pubmed/?term=3827521">A 2.5-year follow-up of cocaine use among treated opioid addicts. Have our treatments helped?</a>."</span>                    <span><em>Arch. Gen. Psychiatry.</em> 1987 Mar;44(3):281-4.</span>
                    Pubmed PMID: <a href="https://ncbi.nlm.nih.gov/pubmed/?term=3827521">3827521</a>                  </li>
                                                                                                <li>
                    <span>Kosten TR, Rounsaville BJ, Kleber HD</span>                    <span>"<a href="https://ncbi.nlm.nih.gov/pubmed/?term=3806731">A 2.5 year follow-up of treatment retention and reentry among opioid addicts.</a>."</span>                    <span><em>J Subst Abuse Treat.</em> 1986;3(3):181-9.</span>
                    Pubmed PMID: <a href="https://ncbi.nlm.nih.gov/pubmed/?term=3806731">3806731</a>                  </li>
                                                                                                <li>
                    <span>Kosten TR, Rounsaville BJ, Kleber HD</span>                    <span>"<a href="https://ncbi.nlm.nih.gov/pubmed/?term=3729667">A 2.5-year follow-up of depression, life crises, and treatment effects on abstinence among opioid addicts.</a>."</span>                    <span><em>Arch Gen Psychiatry.</em> 1986 Aug;733-8.</span>
                    Pubmed PMID: <a href="https://ncbi.nlm.nih.gov/pubmed/?term=3729667">3729667</a>                  </li>
'''
url = "https://www.bcm.edu/people-search/thomas-kosten-24837"
response = requests.get(url,verify=False)
html = response.text
pubmed_data = get_pubmed_data(html)

# Convert to JSON
result = {"pubmed": pubmed_data}
json_result = json.dumps(result, indent=4)
print(json_result)

# import html2markdown
#
#
with open("data/SHIH-JUNG-CHENG_html.txt", "r", encoding="utf8") as f:
    text = f.read()
# # print(html2markdown.convert('<h2>Test</h2><pre><code>Here is some code</code></pre>'))
# print(html2markdown.convert(text))


import html2text

print(html2text.html2text(text))

with open("data/SHIH-JUNG-CHENG_html_md.txt","w",encoding="utf8") as f:
    f.write(html2text.html2text(text))
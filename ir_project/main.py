import re
import io
import os
import requests
import mwparserfromhell

pages = ['George_Orwell|Douglas_Adams|Ted_Chiang|Neil_Gaiman|Oscar_Wilde|Doris_Dana|Peter_Ackroyd|John_Boswell|George_R._R._Martin|Dan_Brown|Thomas_Bulfinch|J._K._Rowling|Dante_Alighieri|Margaret_Atwood|Stephen_King']

baseurl = 'http://en.wikipedia.org/w/api.php'
my_atts = {}
my_atts['action'] = 'query'
my_atts['prop'] = 'revisions'
#my_atts['prop'] = 'extracts'
#my_atts['exintro'] = 'True'
#my_atts['explaintext'] = 'True'
my_atts['rvprop'] = 'content'
#my_atts['rvsection'] = '0'
my_atts['format'] = 'json'
my_atts['titles'] = pages

resp = requests.get(baseurl, params=my_atts)

pages = resp.json()
pages = (pages.get('query')).get('pages')

for page in pages:
    title = (pages[page]).get('title')
    print(title)

    revisions = (pages[page]).get('revisions')
    content = revisions[0].get("*")
    parsed_wikicode = mwparserfromhell.parse(content)
    content = parsed_wikicode

    content = parsed_wikicode.strip_code()

    file = io.open("corpus/"+title+".txt", "w", encoding="utf-8")
    fileNew = io.open("corpus/"+title, "w", encoding="utf-8")

    sentences = re.split(r'(?<!\s\w)\.\s*', content)
    for sentence in sentences:
        sentence = sentence.replace(';','').replace('"','')
        if sentence not in ['\n', '', ' ','.']:
            fileNew.write(sentence + "\n")

    fileNew.close()

    lines = io.open("corpus/" + title, 'r', encoding="utf-8")

    for line in lines:

        if ("Category:" not in line):
            if not line.strip(): continue
            file.write(line)

    os.remove("corpus/"+title)

    print('==========================================================================================')

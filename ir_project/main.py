import re
import io
import os
import requests
import mwparserfromhell

pages = ['George_Orwell|Douglas_Adams|Bernard_Cornwell|Neil_Gaiman|Doris_Dana|Peter_Ackroyd|John_Boswell|George_R._R._Martin|Dan_Brown|J._K._Rowling|Margaret_Atwood|Stephen_King|Ernest_Hemingway|Suzanne_Collins']

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

    file = io.open("corpus/" + title + "_old", "w", encoding="utf-8")
    file.write(content)
    file.close()

    lines = io.open("corpus/" + title + "_old", 'r', encoding="utf-8")

    newFile = io.open("corpus/" + title, "w", encoding="utf-8")
    for line in lines:
        if ("Category:" not in line):
            if not line.strip(): continue
            newFile.write(line)

    newFile.close()

    os.remove("corpus/" + title + "_old")

    print('==========================================================================================')

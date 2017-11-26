import re
import requests
import mwparserfromhell

pages = ['George_Orwell|Douglas_Adams|Ted_Chiang|Neil_Gaiman|George_R._R._Martin|Dan_Brown|Thomas_Bulfinch|J._K._Rowling|Dante_Alighieri|Margaret_Atwood|Stephen_King|Doris_Dana|Peter_Ackroyd|John_Boswell']

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
    content = parsed_wikicode.strip_code()

    file = open("corpus/"+title,'w')
    content = content.encode('utf-8')
    file.write(content)
    file.close()
    print('==========================================================================================')

import json
import requests

pages = ['George_Orwell|Neil_Gaiman|George_R._R._Martin|Dan_Brown|Thomas_Bulfinch|Ted_Chiang|Margaret_Atwood|Stephen_King|Doris_Dana|Peter_Ackroyd|John_Boswell|Jamie_O%27Neill']

baseurl = 'http://en.wikipedia.org/w/api.php'
my_atts = {}
my_atts['action'] = 'query'
my_atts['prop'] = 'revisions'
my_atts['rvprop'] = 'content'
#my_atts['rvsection'] = '0'
my_atts['format'] = 'json'
my_atts['titles'] = pages

resp = requests.get(baseurl, params=my_atts)

pages = resp.json()
pages = (pages.get('query')).get('pages')

for page in pages:

    #title = (pages[page]).get('title')
    #print(title)
    revisions = (pages[page]).get('revisions')
    content = revisions[0].get("*")

    print(content)
    print('==========================================================================================')